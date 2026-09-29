import math


def paper_area(length: float, width: float, height: float, overlap: float = 1.15) -> dict:
    L, W, H = float(length), float(width), float(height)
    if min(L, W, H) <= 0:
        raise ValueError("box dimensions must be positive")
    base = 2 * (L * W + L * H + W * H)
    need = base * float(overlap)
    return {"box_surface": round(base, 3), "overlap": float(overlap), "paper_m2": round(need, 3)}


def sheet_cut(paper_m2: float, roll_width: float) -> dict:
    """卷宽下料：先按卷宽把面积切成料长，再按单张 1m 向上取整得张数。"""
    rw = float(roll_width)
    if rw <= 0:
        raise ValueError("roll_width must be positive")
    sheet_len = float(paper_m2) / rw
    sheets = math.ceil(sheet_len - 1e-9)
    if sheets < 1:
        sheets = 1
    return {"roll_width": rw, "sheet_len": round(sheet_len, 3), "sheets": sheets}


def ribbon_estimate(length: float, width: float, height: float, wrap_style: str = "cross") -> dict:
    """Helper: approximate ribbon length in meters (not stored as primary metric)."""
    L, W, H = float(length), float(width), float(height)
    girth = 2 * (W + H)
    if wrap_style == "band":
        meters = girth + 0.3
    else:
        meters = girth * 2 + L + 0.5
    return {"wrap_style": wrap_style, "ribbon_m": round(meters, 2)}
