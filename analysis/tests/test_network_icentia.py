"""Optional: reads one real Icentia11k segment from PhysioNet (run with -m network)."""
import pytest

pytestmark = pytest.mark.network


def test_real_segment():
    import wfdb
    from esvea.ingest.tables import beats_from_annotation, intervals_from_beats
    a = wfdb.rdann("p00000_s00", "atr", pn_dir="icentia11k-continuous-ecg/1.0/p00/p00000")
    b = beats_from_annotation(a.sample, a.symbol, a.aux_note)
    iv = intervals_from_beats(b)
    assert len(b) > 1000 and iv.tally.mean() > 0.5
