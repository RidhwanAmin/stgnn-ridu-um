import numpy as np
import pytest

from esvea.ro1.filters import percent_deviation, percent_deviation_by_segment


def test_steady_rhythm_all_kept():
    assert percent_deviation(np.full(50, 0.8), 0.2).all()


def test_premature_beat_and_pause_removed():
    rr = np.full(30, 0.8)
    rr[10], rr[11] = 0.5, 1.1          # PAC coupling (-37.5%) and the pause after it (+37.5%)
    keep = percent_deviation(rr, 0.2)
    assert not keep[10] and not keep[11] and keep[12]


def test_reference_restarts_per_segment():
    rr = np.r_[np.full(10, 0.6), np.full(10, 1.0)]
    seg = np.r_[np.zeros(10), np.ones(10)]
    assert percent_deviation_by_segment(rr, seg, 0.2).all()
    assert not percent_deviation(rr, 0.2)[10]


def test_adaptive_flags_ectopic():
    pytest.importorskip("neurokit2")
    from esvea.ro1.filters import adaptive_lipponen_tarvainen
    rng = np.random.default_rng(0)
    rr = 0.8 + rng.normal(0, 0.01, 300)
    rr[150], rr[151] = 0.5, 1.1
    keep = adaptive_lipponen_tarvainen(rr)
    assert not keep[150] or not keep[151]
    assert keep.mean() > 0.95
