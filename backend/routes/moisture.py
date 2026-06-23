import os

from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

TEMPLATE_DIR = os.path.abspath(
    os.path.join(BASE_DIR, "../../frontend/templates")
)

print("Moisture Template Folder:", TEMPLATE_DIR)

templates = Jinja2Templates(directory=TEMPLATE_DIR)


@router.get("/moisture", response_class=HTMLResponse)
async def moisture_page(request: Request):

    user = request.session.get("user")

    if not user:
        return RedirectResponse("/", status_code=302)

    return templates.TemplateResponse(
        "moisture.html",
        {
            "request": request,
            "user": user
        }
    )


@router.post("/moisture", response_class=HTMLResponse)
async def predict_moisture(
    request: Request,
    temperature: float = Form(...),
    humidity: float = Form(...)
):

    user = request.session.get("user")

    if not user:
        return RedirectResponse("/", status_code=302)

    moisture = round((humidity * 0.7) + (temperature * 0.3), 2)

    return templates.TemplateResponse(
        "moisture.html",
        {
            "request": request,
            "user": user,
            "temperature": temperature,
            "humidity": humidity,
            "moisture": moisture
        }
    )