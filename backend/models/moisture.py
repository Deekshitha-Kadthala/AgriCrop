from fastapi import APIRouter
from fastapi import Request
from fastapi import Form
from fastapi.responses import HTMLResponse
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from models.moisture import predict_moisture

router = APIRouter()

templates = Jinja2Templates(
    directory="../frontend/templates"
)


@router.get(
    "/moisture",
    response_class=HTMLResponse
)
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


@router.post("/moisture")
async def predict_moisture(

    crop: str = Form(...),

    temperature: float = Form(...),

    humidity: float = Form(...),

    rainfall: float = Form(...)

):

    moisture = (humidity * 0.5) + (rainfall * 0.3) - (temperature * 0.2)

    if moisture >= 60:

        level = "High"

        advice = "No irrigation required today."

    elif moisture >= 35:

        level = "Medium"

        advice = "Light irrigation is recommended."

    else:

        level = "Low"

        advice = "Immediate irrigation is required."

    return {

        "crop": crop,

        "temperature": temperature,

        "humidity": humidity,

        "rainfall": rainfall,

        "moisture": round(moisture, 2),

        "level": level,

        "advice": advice

    }