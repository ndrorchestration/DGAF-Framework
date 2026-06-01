"""
INV-03 Credit Proxy Signal Corpus
Anchor: S068 | Pattern: P-35 (Procluding Premise Gate) | Blockers: BLG-P35-01

Purpose: Domain-specific premise_check_fn for OI-01 (credit proxy detection).
Each entry: (phrase, weight, rationale).
Weight 1.0 = strong proxy signal. Weight 0.5 = weak / contextual signal.
"""
from typing import List, Tuple

SignalEntry = Tuple[str, float, str]

CREDIT_SIGNALS: List[SignalEntry] = [
    # --- ZIP / Geography proxies ---
    ("zip code",              1.0, "Geographic redlining proxy; highly correlated with race in US lending"),
    ("neighborhood",          0.8, "Neighborhood composition proxies for racial demographics"),
    ("school district",       0.7, "School district boundaries often reflect historical segregation"),
    ("census tract",          0.8, "Census tract demographic composition is a known proxy variable"),
    ("area code",             0.6, "Area code used as coarse geographic proxy in some legacy models"),

    # --- Social graph / behavioral proxies ---
    ("friends who defaulted", 1.0, "Peer default rate — explicit social graph credit discrimination (CFPB flagged)"),
    ("social network",        0.8, "Social network features can encode protected class membership"),
    ("contact list",          0.9, "Contact list analysis as proxy for socioeconomic cohort"),
    ("shopping behavior",     0.7, "Purchase category patterns proxy for income and demographic group"),
    ("browsing history",      0.7, "Web browsing proxies for interest, health status, and demographics"),

    # --- Employment / education proxies ---
    ("alma mater",            0.9, "College attended correlates with race and socioeconomic background"),
    ("employer name",         0.7, "Employer proxies for industry, income class, and demographic composition"),
    ("job title",             0.6, "Occupational segregation makes job title a partial demographic proxy"),
    ("graduation year",       0.6, "Graduation year can proxy for age; age correlated with protected characteristics"),

    # --- Name / language proxies ---
    ("first name",            1.0, "Given name strongly proxies for race and national origin (Bertrand & Mullainathan 2004)"),
    ("last name",             0.9, "Surname proxies for national origin, ethnicity"),
    ("language preference",   0.8, "Language preference proxies for national origin / immigrant status"),

    # --- Device / channel proxies ---
    ("device type",           0.6, "Device brand/type proxies for income tier"),
    ("app store",             0.5, "iOS vs Android usage correlates with income demographics in US"),

    # --- Financial behavior edge cases ---
    ("payday loan",           0.7, "Payday loan usage correlates with low income — disparate impact risk in scoring"),
]


def premise_check_fn_credit(text: str) -> bool:
    """
    P-35 premise_check_fn for OI-01 (credit domain).
    Returns True if any high-weight (>=0.7) proxy signal is detected in text.
    """
    text_lower = text.lower()
    return any(
        weight >= 0.7 and phrase in text_lower
        for phrase, weight, _ in CREDIT_SIGNALS
    )
