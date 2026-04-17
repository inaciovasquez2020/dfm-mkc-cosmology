from pathlib import Path

def test_next_closure_move_doc():
    p = Path("docs/status/NEXT_CLOSURE_MOVE.md")
    s = p.read_text()
    assert "authentic external datasets" in s
    assert "No synthetic placeholder fallback" in s
    assert "Tagged public release created" in s
