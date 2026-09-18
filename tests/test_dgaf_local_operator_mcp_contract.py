from __future__ import annotations

import ast
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ADAPTER = ROOT / "scripts/dgaf_local_operator_mcp.py"
EXPECTED_TOOLS = {"status", "verify_inputs", "materialize", "get_evidence"}


def parse_adapter() -> tuple[str, ast.Module]:
    source = ADAPTER.read_text(encoding="utf-8")
    return source, ast.parse(source)


def tool_functions(tree: ast.Module) -> dict[str, ast.FunctionDef]:
    result: dict[str, ast.FunctionDef] = {}
    for node in tree.body:
        if not isinstance(node, ast.FunctionDef):
            continue
        for decorator in node.decorator_list:
            if (
                isinstance(decorator, ast.Call)
                and isinstance(decorator.func, ast.Attribute)
                and isinstance(decorator.func.value, ast.Name)
                and decorator.func.value.id == "mcp"
                and decorator.func.attr == "tool"
            ):
                result[node.name] = node
    return result


def test_adapter_exposes_exact_four_tool_allowlist() -> None:
    _, tree = parse_adapter()
    assert set(tool_functions(tree)) == EXPECTED_TOOLS


def test_adapter_tools_accept_no_user_arguments() -> None:
    _, tree = parse_adapter()
    for function in tool_functions(tree).values():
        assert function.args.args == []
        assert function.args.kwonlyargs == []
        assert function.args.vararg is None
        assert function.args.kwarg is None


def test_adapter_delegates_to_existing_bridge_dispatch() -> None:
    _, tree = parse_adapter()
    tools = tool_functions(tree)

    for name, function in tools.items():
        returns = [node for node in ast.walk(function) if isinstance(node, ast.Return)]
        assert len(returns) == 1
        call = returns[0].value
        assert isinstance(call, ast.Call)
        assert isinstance(call.func, ast.Name)
        assert call.func.id == "dispatch"
        assert len(call.args) == 1
        request = call.args[0]
        assert isinstance(request, ast.Dict)
        assert len(request.keys) == 1
        assert isinstance(request.keys[0], ast.Constant)
        assert request.keys[0].value == "action"
        assert isinstance(request.values[0], ast.Constant)
        assert request.values[0].value == name


def test_adapter_runs_stdio_only() -> None:
    source, tree = parse_adapter()
    main = next(node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name == "main")
    calls = [node for node in ast.walk(main) if isinstance(node, ast.Call)]
    run_calls = [
        node
        for node in calls
        if isinstance(node.func, ast.Attribute)
        and isinstance(node.func.value, ast.Name)
        and node.func.value.id == "mcp"
        and node.func.attr == "run"
    ]
    assert len(run_calls) == 1
    assert len(run_calls[0].args) == 1
    assert isinstance(run_calls[0].args[0], ast.Constant)
    assert run_calls[0].args[0].value == "stdio"

    lowered = source.lower()
    assert "streamable-http" not in lowered
    assert "run_sse" not in lowered
    assert "socket" not in lowered


def test_adapter_has_no_process_or_filesystem_escape_imports() -> None:
    _, tree = parse_adapter()
    imported: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imported.update(alias.name.split(".")[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            imported.add(node.module.split(".")[0])

    assert "subprocess" not in imported
    assert "socket" not in imported
    assert "requests" not in imported
    assert "httpx" not in imported
