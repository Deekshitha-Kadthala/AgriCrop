from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from backend.database.mongodb import prediction_collection
from backend.models.recommendation import recommendations
import os

router = APIRouter()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

templates = Jinja2Templates(
    directory=os.path.abspath(
        os.path.join(BASE_DIR, "..", "frontend", "templates")
    )
)

@router.get("/report", response_class=HTMLResponse)
async def report_page(request: Request):

    user = request.session.get("user")

    if not user:
        return RedirectResponse("/", status_code=302)

    reports = list(
        prediction_collection.find(
            {"email": user["email"]}
        ).sort("uploaded_at", -1)
    )

    print("Reports Found:", len(reports))

    for report in reports:

        disease = report["prediction"]["disease"]

        report["recommendation"] = recommendations.get(
            disease,
            {
                "description": "-",
                "treatment": "-",
                "fertilizer": "-",
                "irrigation": "-",
                "precautions": "-"
            }
        )

    return templates.TemplateResponse(
        "report.html",
        {
            "request": request,
            "user": user,
            "reports": reports
        }
    )