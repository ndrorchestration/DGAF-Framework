"""
INV-03 Justice Recidivism Signal Corpus
Anchor: S068 | Pattern: P-35 (Procluding Premise Gate) | Blockers: BLG-P35-01

Purpose: Domain-specific premise_check_fn for OI-02 (justice / recidivism domain).
Each entry: (phrase, weight, rationale).
Weight 1.0 = strong proxy signal. Weight 0.5 = contextual / lower confidence.

References: ProPublica COMPAS analysis (2016), Dressel & Farid (2018),
            Chouldechova (2017 fairness impossibility), Kleinberg et al. (2016).
"""
from typing import List, Tuple

SignalEntry = Tuple[str, float, str]

JUSTICE_SIGNALS: List[SignalEntry] = [
    # --- Geography / residential proxies ---
    ("home address",          0.9, "Residential address proxies for race via segregated neighborhoods"),
    ("zip code",              1.0, "ZIP code is a first-order race proxy in US criminal justice datasets"),
    ("neighborhood crime rate", 0.9, "Neighborhood crime rate encodes historical over-policing of minority areas"),
    ("census tract",          0.8, "Census tract demographic composition proxies for race"),

    # --- Social graph / peer proxies ---
    ("criminal associates",   1.0, "Network of criminal associates — COMPAS-style feature with disparate impact"),
    ("family criminal history", 0.9, "Family criminal history penalizes defendants for relatives’ conduct"),
    ("peer group",            0.7, "Peer group composition proxies for socioeconomic cohort and race"),
    ("social ties",           0.7, "Social tie features in risk scores encode demographic disparities"),

    # --- Employment / economic instability proxies ---
    ("unemployment",          0.8, "Unemployment status correlates with race due to structural barriers"),
    ("unstable employment",   0.8, "Employment instability is a proxy for poverty and racial disparity"),
    ("eviction history",      0.8, "Eviction records highly correlated with race in US housing data"),
    ("public assistance",     0.9, "Public assistance receipt proxies for poverty and protected class membership"),

    # --- Education proxies ---
    ("education level",       0.7, "Educational attainment correlates with race due to structural inequities"),
    ("school disciplinary",   0.8, "School discipline records reflect racial disparities in zero-tolerance policies"),
    ("suspension",            0.7, "School suspension rate is a known racial disparity signal"),

    # --- Age / prior contact proxies ---
    ("first arrest age",      0.8, "Age at first arrest encodes differential policing exposure, not just behavior"),
    ("prior arrests",         0.9, "Prior arrest count reflects over-policing rather than actual offending rates"),
    ("juvenile record",       0.9, "Juvenile record usage in adult sentencing has documented disparate racial impact"),

    # --- Attitude / self-report proxies ---
    ("attitudes toward crime", 0.7, "Self-reported attitude scales can proxy for cultural background and race"),
    ("substance abuse",       0.6, "Substance abuse history correlates with race in arrest and treatment data"),

    # --- Instrument-specific ---
    ("compas score",          1.0, "COMPAS risk score directly — known to produce racially disparate false positive rates"),
]


def premise_check_fn_justice(text: str) -> bool:
    """
    P-35 premise_check_fn for OI-02 (justice / recidivism domain).
    Returns True if any high-weight (>=0.7) proxy signal is detected in text.
    """
    text_lower = text.lower()
    return any(
        weight >= 0.7 and phrase in text_lower
        for phrase, weight, _ in JUSTICE_SIGNALS
    )
