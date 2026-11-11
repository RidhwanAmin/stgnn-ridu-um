"""RQ1.3 on P1: premature (S+V) vs PAC-only (S) daily-equivalent counts by burden band."""
from esvea.config import RESULTS
from esvea.io import load_summary
from esvea.ro1.origin import by_band, origin_table
from esvea.ro1.retention import add_burden_band

tab = origin_table(add_burden_band(load_summary(["P1"], "rq13")))
RESULTS.mkdir(exist_ok=True)
tab.to_parquet(RESULTS / "rq13_P1.parquet", index=False)
print(by_band(tab).to_string(index=False))
