# Governed Repo v0 outside-operator trial

Status: **controlled usability trial / package path / non-mutating**

Controller: GitHub issue #1210.

This exercise tests whether one technically capable operator who did not build
Governed Repo can install and use the package from public instructions alone.

It is not a certification, security assessment, production approval, or
independent scientific validation.

## Rules for the trial

The operator should:

- not be the implementation author;
- not rely on private NDR ecosystem context;
- not receive step-by-step coaching from the implementation author;
- record any ambiguity, failed command, hidden assumption, or needed
  clarification instead of silently working around it.

If a blocking defect appears, record it. A defect is useful usability evidence.

## Validated source under test

Use this exact source commit:

```text
4738619157aa6ace9ed13bb56bec4721be5d35ef
```

This exact commit completed the Governed Repo package workflow successfully on
Python 3.10, 3.11, 3.12, 3.13, and 3.14, along with all repository-wide
pull-request workflows returned for the head.

The package is not published. Install it from the exact source checkout.

## 1. Prerequisites

You need:

- Git;
- Python 3.10 or newer;
- pip.

Record your operating system and Python version before continuing:

```bash
python --version
git --version
```

## 2. Clone and pin the exact source

```bash
git clone https://github.com/ndrorchestration/DGAF-Framework.git
cd DGAF-Framework
git checkout 4738619157aa6ace9ed13bb56bec4721be5d35ef
git rev-parse HEAD
```

Expected final SHA:

```text
4738619157aa6ace9ed13bb56bec4721be5d35ef
```

If the SHA differs, stop and record the mismatch.

## 3. Create an isolated environment

### Windows PowerShell

```powershell
python -m venv .venv-governed-repo
.\.venv-governed-repo\Scripts\python.exe -m pip install --upgrade pip
.\.venv-governed-repo\Scripts\python.exe -m pip install .\packages\governed-repo
```

For the remaining Windows commands, replace `python` with:

```text
.\.venv-governed-repo\Scripts\python.exe
```

### macOS or Linux

```bash
python -m venv .venv-governed-repo
./.venv-governed-repo/bin/python -m pip install --upgrade pip
./.venv-governed-repo/bin/python -m pip install ./packages/governed-repo
```

For the remaining macOS/Linux commands, replace `python` with:

```text
./.venv-governed-repo/bin/python
```

## 4. Verify the installed package

Run:

```bash
python -c "import governed_repo; print(governed_repo.PromotionReason.ELIGIBLE_FOR_PROMOTION.value)"
```

Expected output:

```text
ELIGIBLE_FOR_PROMOTION
```

Record whether this worked without changing the instructions.

## 5. Run an eligible case

Create a file named `outside_operator_trial.py` with this content:

```python
from governed_repo import (
    ChangeIdentity,
    GateReceipt,
    GateRequirement,
    PromotionPolicy,
    assess_promotion,
)

identity = ChangeIdentity(
    repository="example/repository",
    change_id="trial-1",
    base_sha="base-123",
    head_sha="head-456",
    observed_base_sha="base-123",
    observed_head_sha="head-456",
    observed_at="2026-10-01T18:00:00Z",
)

policy = PromotionPolicy(
    required_gates=(
        GateRequirement(
            gate_id="tests",
            gate_class="quality",
            require_head_binding=True,
        ),
    ),
)

receipt = GateReceipt(
    gate_id="tests",
    status="completed",
    conclusion="success",
    observed_at="2026-10-01T18:00:00Z",
    head_sha="head-456",
)

result = assess_promotion(identity, policy, [receipt])
print(result.to_dict())
```

Run it:

```bash
python outside_operator_trial.py
```

The result should include:

```text
eligible: true
reason_code: ELIGIBLE_FOR_PROMOTION
merge_executed: false
mutation_executed: false
authorization_effect: NONE
```

The exact Python dictionary formatting may differ, but those values should be
present.

## 6. Run a denial case

In the same file, change only:

```python
observed_base_sha="older-base",
```

Run the file again.

The result should now include:

```text
eligible: false
reason_code: STALE_BASE
merge_executed: false
mutation_executed: false
authorization_effect: NONE
```

Do not "fix" the denial. The expected denial is part of the test.

## 7. Explain the result without consulting the author

In your own words, answer:

1. What does `ELIGIBLE_FOR_PROMOTION` mean here?
2. Did Governed Repo merge, push, deploy, release, or mutate anything?
3. Does the receipt itself grant authorization to merge?
4. Why did the second case return `STALE_BASE`?
5. What information would you still need before taking a real repository
   action?

There is no requirement to use particular wording. The important boundary is
that eligibility is understood as an evaluation result, not execution or an
authorization grant.

## 8. Record usability evidence

Copy and complete this record:

```text
Operator role/background (coarse):
Operating system:
Python version:
Trial date:
Exact source SHA:
Installation completed without undocumented steps: YES / NO
Import check passed: YES / NO
Eligible case produced ELIGIBLE_FOR_PROMOTION: YES / NO
Denial case produced STALE_BASE: YES / NO
Non-effect fields remained false/NONE: YES / NO

Did you need help beyond this document?:
If yes, what help?:

Commands or wording that were unclear:
Missing assumptions:
Unexpected errors:
Workarounds attempted:
What would you change in the instructions?:

Your explanation of ELIGIBLE_FOR_PROMOTION:
Your explanation of the non-effect fields:
Your explanation of STALE_BASE:

Overall trial completed without author coaching: YES / NO
```

Attach the completed record to issue #1210 or return it to the project owner
without editing the answers after the fact.

## Pass boundary

This bounded trial is complete only if the operator can, without
implementation-author coaching:

- install the package from the exact source;
- run one eligible case;
- run the expected stale-base denial;
- identify the reason codes;
- correctly understand that the receipt performs no mutation and grants no
  authorization.

A failed or confusing step should be recorded rather than hidden.

## Claim ceiling

One successful trial can establish only:

**bounded outside-operator usability for one operator, one documented package
path, and the tested environment.**

It does not establish:

- generalized usability;
- independent scientific validation;
- production security;
- complete GitHub correctness;
- merge authority;
- compliance or certification;
- High-Assurance authorization;
- publication readiness;
- commercial demand;
- product-market fit.
