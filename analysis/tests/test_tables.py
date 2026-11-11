import numpy as np
import pandas as pd

from esvea.ingest.tables import beats_from_annotation, interval_category, intervals_from_beats, longest_run


def test_rhythm_context_and_beats_only():
    sample = np.array([0, 10, 250, 500, 600, 750, 1000])
    symbol = ["+", "N", "N", "+", "N", "S", "Q"]
    aux = ["(N", "", "", "(AFIB", "", "", ""]
    b = beats_from_annotation(sample, symbol, aux)
    assert list(b.cls) == ["N", "N", "N", "S", "Q"]
    assert list(b.in_af) == [False, False, True, True, True]


def test_intervals_tally_and_categories():
    b = pd.DataFrame({"sample": [0, 200, 325, 600, 2000], "cls": ["N", "N", "S", "N", "Q"], "in_af": [False] * 5})
    iv = intervals_from_beats(b, fs=250)
    iv["category"] = interval_category(iv)
    assert list(iv.category) == ["normal", "pac_coupling", "pause_after_pac", "other"]
    assert list(iv.tally) == [True, True, True, False]       # last touches Q (and is 5.6 s)


def test_longest_run():
    assert longest_run(np.array(list("NSSSNSS"))) == 3
