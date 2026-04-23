from pathlib import Path

def test_next_closure_move_doc():
    s = Path("docs/status/NEXT_CLOSURE_MOVE.md").read_text(encoding="utf-8")
    assert "none" in s
    assert "All satisfied." in s
