from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.repositories import papers as repo
router = APIRouter()


class PaperUpdate(BaseModel):
    name: str | None = None
    roll_width: float | None = None


@router.get("/papers")
def list_papers(): return {"items": repo.list_papers()}


@router.get("/papers/{pid}")
def get_paper(pid: int):
    p = repo.get_paper(pid)
    if not p:
        raise HTTPException(404)
    return p


@router.put("/papers/{pid}")
def update_paper(pid: int, body: PaperUpdate):
    if body.roll_width is not None and body.roll_width <= 0:
        raise HTTPException(422, "roll_width must be positive")
    if not repo.get_paper(pid):
        raise HTTPException(404)
    repo.update_paper(pid, body.name, body.roll_width)
    return repo.get_paper(pid)
