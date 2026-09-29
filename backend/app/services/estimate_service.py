from fastapi import HTTPException
from app.engines.wrap_math import paper_area, ribbon_estimate, sheet_cut
from app.repositories import boxes, history, papers, settings_repo


def run_estimate(box_id: int, paper_id: int, overlap: float | None, wrap_style: str, save: bool, note: str):
    box = boxes.get_box(box_id)
    if not box:
        raise HTTPException(404)
    if box.get("data_quality") == "dirty":
        raise HTTPException(422, "dirty box")
    paper = papers.get_paper(paper_id)
    if not paper:
        raise HTTPException(422, "paper roll not found")
    roll_width = paper.get("roll_width")
    if roll_width is None or float(roll_width) <= 0:
        raise HTTPException(422, "invalid roll_width")
    ov = float(overlap) if overlap is not None else settings_repo.get_overlap()
    calc = paper_area(box["length"], box["width"], box["height"], ov)
    cut = sheet_cut(calc["paper_m2"], roll_width)
    ribbon = ribbon_estimate(box["length"], box["width"], box["height"], wrap_style)
    payload = {
        **calc,
        **cut,
        "ribbon": ribbon,
        "wrap_style": wrap_style,
        "box_id": box_id,
        "paper_id": paper_id,
        "paper_name": paper["name"],
    }
    run_id = history.insert_run(box_id, ov, payload, note) if save else None
    return {"box": box, "run_id": run_id, **calc, **cut, "ribbon": ribbon,
            "paper_id": paper_id, "paper_name": paper["name"]}
