# Synthetic containment assessment V0

This candidate adds explicit meanings for bounded containment claims. It reports what supplied synthetic evidence establishes, which predicates remain unknown or contradicted, and why the record grants no execution authority.

`scripts.dgaf_containment_assessment.assess(contract, observation, now=aware_datetime)` checks strict definition/scope binding, complete categorical predicates, evidence references and snapshot freshness. Dispositions are ESTABLISHED_IN_SCOPE, NOT_ESTABLISHED and CONTRADICTED_IN_SCOPE. In-scope historical contradictions remain visible alongside stale/unknown reasons; foreign or changed-definition evidence cannot establish this scope.

`scripts.dgaf_containment_observation.assess_bound_snapshot(contract, raw_bytes, expected_observation_digest=separate_pin, now=aware_datetime)` also requires exact raw-byte SHA256 binding. Observations are UTF-8 JSON objects of 1–65536 bytes. Duplicate keys, malformed encoding, non-finite constants and missing/wrong pins fail closed. Obtain the expected pin outside the submitted record. The API cannot authenticate the caller's pin or its producer; matching a digest is not independent attestation. In-process mappings should not be concurrently mutated during assessment.

Timestamp format is YYYY-MM-DDTHH:MM:SS[.fraction](Z|±HH:MM), with at most six fractional digits and valid calendar/offset components. Higher precision is rejected rather than silently truncated. The fixture's 30-second age limit is a synthetic policy choice.

Every disposition retains authority_effect=NONE, follow_on_authority=FRESH_ADJUDICATION_REQUIRED, execution_permitted=false, scientific_n_increment=0. Reused protected-effect PEP refusal is tested using the actual established assessment record; no receipt-to-permission transfer is introduced.

Generate the checked-in Tektite replay from separately pinned fixture bytes:

```bash
python -m scripts.generate_tektite_containment
python -m pytest tests/test_containment*.py tests/test_capability_governance_pep.py tests/test_tektite_dgaf_acp_replay_surface.py -q
npm run test:ui
```

Browser failure-path tests live in `app/lib/containment-browser.test.ts`. Set `DGAF_PLAYWRIGHT_MODULE` to an installed Playwright module and `DGAF_CHROMIUM_EXECUTABLE` to its browser executable, then run `npm run test:ui`. Without those inputs, two browser tests are explicitly skipped; Node parser tests still run. With the browser configured, the tests make a real HTTP module request fail with 503 and verify the unavailable state, then check that normal loading renders five validated cases. No new production dependency is introduced.

The demo page links `/evidence/tektite-containment-v0.html`. Its five fixed-time cases are synthetic historical replay, not live monitoring. JSON retains exact implementation digests, definition and observation digests, reasons and authority limits. The static page defaults to Evidence unavailable; failed module loading cannot leave an indefinite loading message. Validation preserves that fallback until success and replaces it with an unavailable state on failure. Text rendering does not interpret evidence strings as markup. The browser does not authenticate the published page or its source hashes. Regenerate after implementation changes, then commit generated assets with their source. Tests require byte-for-byte equivalence of the retained HTML and regenerated UTF-8 output, alongside JSON equivalence.

The existing SBCF research draft #1339 was inspected at `4756929bfe9fb2fa8d42c49a86708f3f1caa5229`. Its signature, source coverage, durable replay and witness prototypes are related evidence-admission work. This assessment does not depend on those unmerged modules or promote their shared-key simulation to independently trusted custody. ACP/AOSS interfaces and accepted Tektite replay remain unchanged.

Remaining admission work: protected-branch checks/review. Remaining trust work: authenticated producer identity, admitted observer/driver/environment coverage, separately provisioned and governed trust anchors, durable receipt binding and independent review. OS/process/network containment and live cross-system integration remain unestablished. N=0; independent validation and canonical efficacy NOT_ESTABLISHED; high assurance NOT_AUTHORIZED.
