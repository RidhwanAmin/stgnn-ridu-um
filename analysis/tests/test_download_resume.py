from esvea.ingest.download import done_patients


def test_done_patients_reads_manifest(tmp_path):
    m = tmp_path / "MANIFEST.sha256"
    assert done_patients(m) == set()
    m.write_text("ab12  p00/p00008/p00008_s00.hea\n"
                 "cd34  p00/p00008/p00008_s00.atr\n"
                 "ef56  p04\\p04596\\p04596_s00.hea\n"
                 "\n")
    assert done_patients(m) == {"p00008", "p04596"}
