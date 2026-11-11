"""The training simulator must not share code with the RO4a degradation operators (section 3.6)."""
import ast
from pathlib import Path

SIM = Path(__file__).resolve().parents[1] / "src" / "esvea" / "simulate"


def test_simulate_does_not_import_degrade():
    for f in SIM.rglob("*.py"):
        tree = ast.parse(f.read_text())
        for node in ast.walk(tree):
            names = [a.name for a in node.names] if isinstance(node, ast.Import) else \
                [node.module or ""] if isinstance(node, ast.ImportFrom) else []
            assert not any("degrade" in n for n in names), f
