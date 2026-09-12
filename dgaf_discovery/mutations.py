from copy import deepcopy
from dataclasses import dataclass
from typing import Any, Callable


@dataclass(frozen=True)
class Mutation:
    mutation_id: str
    family: str
    description: str
    apply: Callable[[dict[str, Any]], dict[str, Any]]


def _replace(path: tuple[str, ...], value: Any):
    def mutate(source):
        target = deepcopy(source)
        cursor = target
        for key in path[:-1]:
            child = cursor.get(key)
            if not isinstance(child, dict):
                child = {}
                cursor[key] = child
            cursor = child
        cursor[path[-1]] = value
        return target

    return mutate


def _delete(path: tuple[str, ...]):
    def mutate(source):
        target = deepcopy(source)
        cursor = target
        for key in path[:-1]:
            child = cursor.get(key)
            if not isinstance(child, dict):
                return target
            cursor = child
        cursor.pop(path[-1], None)
        return target

    return mutate


def critical_mutations() -> tuple[Mutation, ...]:
    return (
        Mutation(
            "AUTH-001",
            "authorization",
            "promote authorization",
            _replace(("authorization",), "AUTHORIZED"),
        ),
        Mutation(
            "EVID-001",
            "independence",
            "promote evidence independence",
            _replace(("evidence", "independent"), True),
        ),
        Mutation(
            "PROV-001",
            "provenance",
            "remove predecessor binding",
            _delete(("evidence", "predecessor_sha")),
        ),
        Mutation(
            "N-001",
            "scientific_n",
            "increment scientific N",
            _replace(("scientific_n",), 1),
        ),
        Mutation(
            "FAIL-001",
            "fail_open",
            "convert unknown to pass",
            _replace(("decision",), "PASS"),
        ),
    )
