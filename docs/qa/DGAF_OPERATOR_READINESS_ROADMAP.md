
# DGAF Operator Readiness Roadmap

Status: **BOUNDED PERSONAL ENGINEERING TEST PATH AVAILABLE**  
Current protected-main basis: read `main` at use time. The Windows operator run
recorded on 2026-09-26 passed 19/19 checks at DGAF
`7f610c71f646135e2c767a5a103a11e6ad3ce9dc` with ACP
`dbab7c1afafec524ce7c18157de2089cafe79c87`.

This roadmap defines what “ready for my test” means. It does not attempt to
close every research, production, or external-trust issue in the repository.

## Ordered work

1. **Operator test path — current gate.** Use
   [`DGAF_OPERATOR_SELFTEST.md`](DGAF_OPERATOR_SELFTEST.md) from a fresh full
   clone. Acceptance requires a retained PASS packet, exact DGAF and ACP
   identities, clean worktrees, covered regression checks, deliberate
   fail-closed checks, and preserved claim ceilings.
2. **Custody refusal probe — current correction.** The Windows path must call
   the custody implementation and verify `O_NOFOLLOW_REQUIRED` with no side
   effects. A missing OS primitive alone is not sufficient evidence.
3. **CI reproducibility — next engineering gate.** Issue [#1056](https://github.com/ndrorchestration/DGAF-Framework/issues/1056)
   tracks replacement of Governance CI's mutable bootstrap with an accepted
   hash-locked dependency contract. This is a supply-chain quality correction,
   not a scientific or authorization transition.
4. **Interface reconstruction.** Rebuild the closed stale-lineage Evidence
   Spine work from #849 on current `main`, then reconstruct #850's audience
   journey/mobile containment. Run fresh UI, build, governance, truth-layer,
   and regression checks before accepting either slice. See
   [`docs/ui/UI_CURRENT_STATE.md`](../ui/UI_CURRENT_STATE.md).
5. **Runtime and ecosystem hardening.** Resolve the live CORS probe under #767
   and classify remaining action/dependency bindings through #777/#939. These
   are separate from the personal non-collecting test path.
6. **External validation.** Issue [#929](https://github.com/ndrorchestration/DGAF-Framework/issues/929)
   controls independent reviewer engagement and independently retained replay.
   It remains outstanding after any internal PASS.

## Panel conclusion

The engineering, operator, governance, and roadmap reviews agree that the
narrow personal test can proceed within the non-collecting scope. Internal
passes cover exact identities, environments, and tested behaviors. They do not
establish canonical DGAF efficacy, independent validation, production
certification, or High-Assurance authorization.

The controlling boundary remains:

```text
SCIENTIFIC_N_INCREMENT=0
INDEPENDENT_VALIDATION=NOT_ESTABLISHED
EXTERNAL_VALIDATION=NOT_ESTABLISHED
CANONICAL_DGAF_EFFICACY=NOT_ESTABLISHED
HIGH_ASSURANCE=NOT_AUTHORIZED
```
