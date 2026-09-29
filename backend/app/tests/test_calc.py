from app.engines.wrap_math import paper_area, sheet_cut


def test_overlap_one():
    assert paper_area(1, 1, 1, 1.0)["paper_m2"] == 6.0


def test_area_to_sheets():
    calc = paper_area(1, 1, 1, 1.0)
    cut = sheet_cut(calc["paper_m2"], 1.0)
    assert cut["sheet_len"] == 6.0
    assert cut["sheets"] == 6

