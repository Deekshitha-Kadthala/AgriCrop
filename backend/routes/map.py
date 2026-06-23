from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
import os

router = APIRouter()
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

templates = Jinja2Templates(
    directory=os.path.abspath(
        os.path.join(BASE_DIR, "../../frontend/templates")
    )
)


@router.get("/map", response_class=HTMLResponse)
async def disease_map(request: Request):

    user = request.session.get("user")

    if not user:
        return RedirectResponse("/", status_code=302)

    return templates.TemplateResponse(
        "map.html",
        {
            "request": request,
            "user": user
        }
    )