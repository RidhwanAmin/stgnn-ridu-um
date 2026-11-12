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
    b = pd.DataFrame({"sample": [0, 200, 400, 600, 800, 1000, 1125, 1400, 2800],
                      "cls": ["N"] * 6 + ["S", "N", "Q"], "in_af": [False] * 9})
    iv = intervals_from_beats(b, fs=250)
    iv["category"] = interval_category(iv)
    assert list(iv.category) == ["normal"] * 5 + ["pac_coupling", "pause_after_pac", "other"]
    assert list(iv.tally) == [True] * 7 + [False]            # last touches Q (and is 5.6 s)


def test_overlapping_categories_and_short_segment():
    from esvea.ro1.retention import removal_counts
    b = pd.DataFrame({"sample": [0, 200, 300, 400, 500, 700, 900, 1100, 1300],
                      "cls": ["N", "N", "S", "S", "V", "N", "N", "N", "N"], "in_af": [False] * 9})
    iv = intervals_from_beats(b, fs=250)
    rc = removal_counts(iv, np.ones(len(iv), bool)).set_index("category").n
    assert rc["pac_coupling"] == 2        # N-S and S-S
    assert rc["pause_after_pac"] == 2     # S-S and S-V (S-S counted in both, as in the legacy script)
    assert rc["pvc_coupling"] == 1 and rc["normal"] == 4
    short = intervals_from_beats(b.iloc[:7], fs=250)
    assert not short.tally.any()          # fewer than 8 beats: no tallied intervals


def test_analysable_rule_is_any_non_q_beat():
    from esvea.ingest.tables import is_analysable
    assert not is_analysable({"n_N": 0, "n_S": 0, "n_V": 0, "n_Q": 5505})   # only Q beats (as p08269)
    assert is_analysable({"n_N": 0, "n_S": 0, "n_V": 1, "n_Q": 0})


def test_longest_run():
    assert longest_run(np.array(list("NSSSNSS"))) == 3
