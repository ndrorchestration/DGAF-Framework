"""
Test suite: INV-03 Signal Corpus
Anchor: S068 | Patterns: P-35, P-04
Metrics: >=20 entries per domain; premise_check_fn fires on known signals;
         no false negatives on canonical proxy terms.
"""
import pytest
from pptl.corpus.inv03_credit_signals import CREDIT_SIGNALS, premise_check_fn_credit
from pptl.corpus.inv03_justice_signals import JUSTICE_SIGNALS, premise_check_fn_justice


# --- Corpus size gates ---

def test_credit_corpus_minimum_size():
    assert len(CREDIT_SIGNALS) >= 20, f"Credit corpus has only {len(CREDIT_SIGNALS)} entries"


def test_justice_corpus_minimum_size():
    assert len(JUSTICE_SIGNALS) >= 20, f"Justice corpus has only {len(JUSTICE_SIGNALS)} entries"


# --- Structural integrity ---

def test_credit_entries_are_triples():
    for entry in CREDIT_SIGNALS:
        assert len(entry) == 3, f"Malformed credit entry: {entry}"
        phrase, weight, rationale = entry
        assert isinstance(phrase, str) and phrase
        assert 0.0 <= weight <= 1.0
        assert isinstance(rationale, str) and rationale


def test_justice_entries_are_triples():
    for entry in JUSTICE_SIGNALS:
        assert len(entry) == 3, f"Malformed justice entry: {entry}"
        phrase, weight, rationale = entry
        assert isinstance(phrase, str) and phrase
        assert 0.0 <= weight <= 1.0
        assert isinstance(rationale, str) and rationale


# --- premise_check_fn: credit ---

def test_credit_fires_on_zip_code():
    assert premise_check_fn_credit("We use zip code as a feature in our model.")


def test_credit_fires_on_first_name():
    assert premise_check_fn_credit("Applicant first name is used for identity verification.")


def test_credit_fires_on_friends_who_defaulted():
    assert premise_check_fn_credit("Score adjusted based on friends who defaulted.")


def test_credit_fires_on_alma_mater():
    assert premise_check_fn_credit("The model ingests alma mater from LinkedIn.")


def test_credit_no_false_positive_on_clean_text():
    assert not premise_check_fn_credit("Applicant income and payment history reviewed.")


# --- premise_check_fn: justice ---

def test_justice_fires_on_zip_code():
    assert premise_check_fn_justice("Recidivism risk includes zip code of residence.")


def test_justice_fires_on_compas_score():
    assert premise_check_fn_justice("Defendant compas score was 8 out of 10.")


def test_justice_fires_on_criminal_associates():
    assert premise_check_fn_justice("Model uses criminal associates network size.")


def test_justice_fires_on_prior_arrests():
    assert premise_check_fn_justice("Prior arrests count included as risk factor.")


def test_justice_no_false_positive_on_clean_text():
    assert not premise_check_fn_justice("Defendant showed remorse and has stable housing.")
