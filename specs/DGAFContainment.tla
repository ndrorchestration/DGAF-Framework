---- MODULE DGAFContainment ----
EXTENDS Naturals, TLC

(***************************************************************************)
(* Minimal executable containment model for DGAF's control-plane boundary.  *)
(* This is a model, not a proof of the implementation.                   *)
(***************************************************************************)

CONSTANTS
    Agents,
    MaxTurns

VARIABLES
    phase,
    breaker,
    turn,
    mutationAllowed

vars == <<phase, breaker, turn, mutationAllowed>>

Phases == {"STAGING", "ACTIVE", "FROZEN", "ROLLBACK", "VERIFIED"}

Init ==
    /\ phase = "STAGING"
    /\ breaker = FALSE
    /\ turn = 0
    /\ mutationAllowed = FALSE

Activate ==
    /\ phase = "STAGING"
    /\ breaker = FALSE
    /\ phase' = "ACTIVE"
    /\ breaker' = FALSE
    /\ turn' = turn + 1
    /\ mutationAllowed' = TRUE

OpenBreaker ==
    /\ phase = "ACTIVE"
    /\ breaker = FALSE
    /\ phase' = "FROZEN"
    /\ breaker' = TRUE
    /\ turn' = turn + 1
    /\ mutationAllowed' = FALSE

Rollback ==
    /\ phase = "FROZEN"
    /\ breaker = TRUE
    /\ phase' = "ROLLBACK"
    /\ breaker' = TRUE
    /\ turn' = turn + 1
    /\ mutationAllowed' = FALSE

Verify ==
    /\ phase = "ROLLBACK"
    /\ breaker = TRUE
    /\ phase' = "VERIFIED"
    /\ breaker' = FALSE
    /\ turn' = turn + 1
    /\ mutationAllowed' = FALSE

Restart ==
    /\ phase = "VERIFIED"
    /\ breaker = FALSE
    /\ phase' = "STAGING"
    /\ breaker' = FALSE
    /\ turn' = turn + 1
    /\ mutationAllowed' = FALSE

Next == Activate \/ OpenBreaker \/ Rollback \/ Verify \/ Restart

TypeOK ==
    /\ phase \in Phases
    /\ breaker \in BOOLEAN
    /\ turn \in Nat
    /\ mutationAllowed \in BOOLEAN

ContainmentInvariant ==
    breaker => /\ phase = "FROZEN" \/ phase = "ROLLBACK"
             /\ mutationAllowed = FALSE

FrozenInvariant ==
    phase = "FROZEN" => mutationAllowed = FALSE

Spec == Init /\ [][Next]_vars /\ WF_vars(Verify)

THEOREM TypeSafety == Spec => []TypeOK
THEOREM ContainmentSafety == Spec => []ContainmentInvariant
THEOREM FrozenSafety == Spec => []FrozenInvariant

====
