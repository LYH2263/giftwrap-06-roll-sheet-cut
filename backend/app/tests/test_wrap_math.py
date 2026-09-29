import pytest
from app.engines.wrap_math import paper_area, ribbon_estimate, sheet_cut


def test_book_box():
    r = paper_area(0.30, 0.20, 0.15, 1.15)
    assert r["box_surface"] == 0.27
    assert r["paper_m2"] == 0.31


def test_ribbon_cross():
    rb = ribbon_estimate(0.30, 0.20, 0.15, "cross")
    assert rb["ribbon_m"] > 0.5


def test_sheet_cut_basic():
    # 0.31 m² on 1.0 m roll -> 0.31 m -> 1 sheet
    r = sheet_cut(0.31, 1.0)
    assert r["roll_width"] == 1.0
    assert r["sheet_len"] == 0.31
    assert r["sheets"] == 1


def test_sheet_cut_multiple_sheets():
    # 1.5 m on 1.0 m roll -> 1.5 m -> 2 sheets
    r = sheet_cut(1.5, 1.0)
    assert r["sheet_len"] == 1.5
    assert r["sheets"] == 2


def test_sheet_cut_narrow_roll():
    # 0.31 m² on 0.7 m roll -> 0.443 m -> 1 sheet
    r = sheet_cut(0.31, 0.7)
    assert r["sheet_len"] == 0.443
    assert r["sheets"] == 1


def test_sheet_cut_exact_meter():
    # exactly 1.0 m -> 1 sheet, no float off-by-one
    r = sheet_cut(1.0, 1.0)
    assert r["sheet_len"] == 1.0
    assert r["sheets"] == 1


def test_sheet_cut_invalid_width():
    with pytest.raises(ValueError):
        sheet_cut(0.31, 0)
    with pytest.raises(ValueError):
        sheet_cut(0.31, -0.7)
