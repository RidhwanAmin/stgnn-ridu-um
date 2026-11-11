import numpy as np

from esvea.pseudodays import assign
from esvea.pulsewatch.matching import best_lag, match_one_to_one, motion_bin
from esvea.simulate.stream import SimConfig, simulate_segment


def test_one_to_one():
    ecg = np.array([1.0, 1.05, 2.0])
    ppg = np.array([1.02, 2.5])
    assert list(match_one_to_one(ecg, ppg)) == [True, False, False]


def test_lag_recovered():
    ecg = np.cumsum(0.8 + np.random.default_rng(4).normal(0, 0.08, 60))   # periodic RR makes the lag ambiguous
    assert abs(best_lag(ecg, ecg + 0.36) - 0.36) < 0.03


def test_motion_bins():
    assert list(motion_bin(np.array([0.01, 0.1, 0.3, 0.7, 2.0]))) == [0, 1, 2, 3, 4]


def test_pseudodays_balanced():
    pd_ = assign(list(range(50)), seed=5)
    assert pd_.pseudo_day.nunique() == 2 and set(pd_.block) == {0, 1, 2, 3}


def test_simulator_accounting():
    rng = np.random.default_rng(0)
    t = np.cumsum(np.full(5000, 0.8))
    cls = np.where(rng.random(5000) < 0.05, "S", "N")
    rep, truth = simulate_segment(t, cls, float(t[-1] + 1), SimConfig(), rng)
    assert truth["n_pac_true"] == (cls == "S").sum()
    assert rep.is_pac.sum() == truth["n_pac_true"] - truth["n_pac_silent"] - truth["n_pac_in_gap"]
    assert rep.flag.any() and not rep.rr[rep.gap_before].notna().any()
    assert 0 < truth["observed_s"] <= t[-1] + 1
