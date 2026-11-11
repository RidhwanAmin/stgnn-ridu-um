import numpy as np
import pandas as pd

from esvea.estimator import equations as eq


def _tau(rows):
    return pd.DataFrame(rows, columns=range(4)).astype(float)


def test_constant_rate_recovered():
    # 10 PACs/h in every block, full coverage, perfect p and retention -> 240/day
    S = _tau([[60, 60, 60, 60]] * 7)
    tau = _tau([[6, 6, 6, 6]] * 7)
    assert np.allclose(eq.daily_rate(S, tau) * 24, 240)
    assert np.isclose(eq.pooled_rate(S, tau) * 24, 240)
    assert eq.esvea_call(eq.pooled_rate(S, tau)) is False


def test_block_weighting_not_coverage_weighting():
    # Night fully covered at 5/h; afternoon thinly covered at 40/h. Daily count weights blocks by L_h, not tau.
    S = _tau([[30, 30, 40, 60]])
    tau = _tau([[6, 6, 1, 6]])
    assert np.isclose(eq.daily_rate(S, tau).iloc[0] * 24, 6 * (5 + 5 + 40 + 10))


def test_gate_and_valid_day():
    tau = _tau([[6, 6, 0.5, 6], [3, 2, 2, 2], [1, 1, 1, 1]])
    assert list(eq.gate(tau)) == [False, True, True]
    assert list(eq.valid_days(tau)) == [True, True, False]


def test_pooled_needs_an_hour_per_block():
    S = _tau([[10, 10, 0, 10]] * 3)
    tau = _tau([[6, 6, 0.2, 6]] * 3)
    assert np.isnan(eq.pooled_rate(S, tau))              # 0.6 h in block 2 across the week
    tau.iloc[:, 2] = 0.5
    assert np.isfinite(eq.pooled_rate(S, tau))


def test_retention_reweighting():
    beats = pd.DataFrame({"day": [0, 0, 0, 0], "block": [0, 1, 2, 3], "p": [1.0] * 4, "pi_hat": [0.5] * 4})
    assert np.allclose(eq.block_sums(beats).to_numpy(), 2.0)


def test_shrinkage_equals_pooled_when_profile_flat_and_full():
    S = _tau([[60, 60, 60, 60]] * 7)
    tau = _tau([[6, 6, 6, 6]] * 7)
    assert np.isclose(eq.shrunk_pooled_rate(S, tau, 1.0, (1, 1, 1, 1)), eq.pooled_rate(S, tau))


def test_schema_validates():
    import pytest
    from esvea.schema import BEAT_COLUMNS, validate
    df = pd.DataFrame({"patient": ["a"], "day": [0], "block": [2], "t": [43300.0], "rr": [0.8],
                       "flag": [False], "motion": [0.03], "gap_before": [False]})
    validate(df, BEAT_COLUMNS)
    with pytest.raises(ValueError):
        validate(df.assign(block=4), BEAT_COLUMNS)
