# DGAF Visual System — Semantic Cohesion Tranche

**Status:** implementation candidate  
**Issue:** #799  
**Scientific/control effect:** NONE  
**Authority effect:** NONE

## Intent

Evolve DGAF from a competent dark control-room interface into a sleek, modern, premium, slightly futuristic governance instrument without changing its truth model.

The visual language should feel plausible today and advanced enough to be recognizably DGAF. Futurism comes from precision, controlled depth, spatial composition, restrained luminosity, geometry, technical typography, and causality-preserving motion — not spectacle.

## Design posture

- Sleek, modern, restrained, premium.
- Slightly futuristic, never cyberpunk.
- Calm authority rather than urgency theater.
- Semantic form before decorative effect.
- Geometry, pattern, line, depth, label, and hierarchy must carry consequential state independently of hue.
- Color accents are sparse and meaning-bound.
- Dark surfaces are dimensional, not flat black.
- Motion communicates causality, hierarchy, or transition and remains equivalent under reduced-motion preferences.

## Semantic token contract

Raw palette names remain implementation primitives. Consequential UI surfaces should consume semantic aliases.

| Semantic role | Purpose |
| --- | --- |
| `state-established` | established predecessor/current governed state |
| `state-frontier` | nearest reachable work / frontier |
| `state-unreachable` | downstream or otherwise unreachable state |
| `boundary-authorization` | explicit authorization/admissibility boundary |
| `boundary-global` | enclosing field/global condition |
| `provenance` | source/evidence lineage and inspectable causal edges |
| `coupling-authority` | authority/escalation relationship |
| `coupling-dependency` | dependency/lateral coupling relationship |
| `evidence` | evidence/source layer |
| `consequence` | affected-scope and consequence treatment |
| `execution-receipt` | action execution / receipt identity |
| `focus-ring` | keyboard/interaction focus |
| `surface-* / text-*` | depth and editorial hierarchy |

These aliases may map to different palette values over time without changing their semantic role.

## Geometry grammar

- **Established state:** stable node/region treatment.
- **Frontier:** structurally emphasized boundary-adjacent region; not a readiness score.
- **Unreachable:** dashed or hatched treatment plus explicit label.
- **Authorization boundary:** band or edge with visible termination of prohibited path.
- **Global constraint:** enclosing frame/field condition.
- **Provenance:** fine inspectable filament, not a decorative connector.
- **Authority coupling:** separate line/pattern grammar from provenance.
- **Dependency coupling:** separate line/pattern grammar from authority.
- **Evidence:** layered stratum/card form distinct from authorization.
- **Receipt:** immutable artifact treatment distinct from evidence existence.
- **Unknown / not modeled:** dotted or explicitly incomplete representation; never low-confidence color alone.

## Typography grammar

1. Orientation: readable sans, generous line-height, plain-language explanation.
2. Governance labels: compact, high-contrast, often mono or small caps.
3. Evidence/provenance identity: mono with stable wrapping and copy affordance.
4. Warnings/boundaries: direct language, no visual panic.
5. Hashes/receipts/runtime identity: mono, visually secondary to the interpreted state.
6. Claim ceilings: editorial treatment distinct from runtime telemetry.

## Surface grammar

Use a small depth vocabulary:

- base field
- raised panel
- inspection surface
- boundary field
- transient/focus surface

Avoid arbitrary card variants. Depth must indicate relationship or inspection hierarchy.

## Motion grammar

Allowed:

- short emphasis transitions when reachability/state changes;
- provenance reveal/tracing;
- expansion/collapse for evidence inspection;
- subtle parallax or field depth only where it clarifies spatial hierarchy.

Avoid:

- ambient pulsing;
- bouncing;
- attention-seeking loops;
- decorative particle systems;
- motion that implies active authority or successful execution.

Reduced-motion mode must preserve the same information and ordering.

## Explicit exclusions

- cyberpunk/gamer HUD visual language
- excessive neon
- holographic ornament
- glassmorphism without hierarchy purpose
- sci-fi display fonts for body or control text
- readiness percentages
- authorization probability/distance
- confidence or efficacy gradients
- generic KPI-dashboard redesign
- completion rings that imply maturity
- glow/saturation as proof, authority, or evidence

## Flagship surfaces

### Decision Frontier

Primary operator handoff. Must make current state, blocking boundary, nearest admissible action, downstream unreachable transitions, provenance, consequence, and receipt state readable without relying on color.

### Governance Map

Primary structural view. Must preserve vertical escalation, lateral coupling, provenance, and global constraints as different visual relationships.

### State Space

Discrete categorical reachability remains authoritative in V0. No continuous geometry, interpolation, readiness distance, confidence field, or efficacy gradient until formal semantics exist.

### Truth Boundary

Must remain the highest-salience compact statement of canonical state and must never be visually subordinated to runtime health.

## QA gates

A tranche fails review if any of these are false:

- Meaning remains legible in grayscale.
- Consequential states have non-color redundancy.
- Narrow/mobile layouts preserve relationships rather than only stacking cards.
- Reduced-motion mode preserves semantic equivalence.
- Focus states are visible.
- Source, runtime, scientific state, and authorization remain distinct.
- Blocked states explain missing prerequisites and nearest admissible work.
- No visual treatment exceeds the underlying claim/evidence ceiling.
- Public/simple mode and operator/expert mode still feel like one product.
