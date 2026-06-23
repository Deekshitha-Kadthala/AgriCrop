from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from backend.database.mongodb import users_collection
from backend.database.mongodb import prediction_collection

router = APIRouter()

templates = Jinja2Templates(
    directory="../frontend/templates"
)


@router.get("/admin", response_class=HTMLResponse)
async def admin_dashboard(request: Request):

    user = request.session.get("user")

    if not user:
        return RedirectResponse("/", status_code=302)

    users = list(users_collection.find())

    predictions = list(prediction_collection.find())

    return templates.TemplateResponse(
        "admin.html",
        {
            "request": request,
            "user": user,
            "users": users,
            "predictions": predictions
        }
    )