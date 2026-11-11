import pytest

from esvea import sets


def test_draw_lock_and_guard(tmp_path, monkeypatch):
    sp = tmp_path / "splits"
    sp.mkdir()
    ids = [f"p{i:05d}" for i in range(100)]
    sets.write_set("P0", ids[:10], 1, sp)
    pool = ids[10:]
    p3 = sets.draw(pool, 20, 7, )
    sets.write_set("P3", p3, 7, sp)
    assert p3 == sets.draw(pool, 20, 7)                       # reproducible from the seed
    with pytest.raises(FileExistsError):
        sets.write_set("P3", p3, 7, sp)
    sets.verify(sp)
    monkeypatch.setitem(sets.ALLOWED, "test", {"P0"})
    g = sets.Guard("test", sp)
    g.check(ids[0])
    with pytest.raises(PermissionError):
        g.check(p3[0])
    with pytest.raises(PermissionError):
        sets.Guard("ro4a", sp)                                 # no M4 freeze record
    (sp / "P3.txt").write_text((sp / "P3.txt").read_text() + "p99999\n")
    with pytest.raises(RuntimeError):
        sets.verify(sp)


def test_p2_split():
    parts = sets.split_p2([f"p{i:05d}" for i in range(1000)], 3)
    assert [len(v) for v in parts.values()] == [700, 150, 150]
