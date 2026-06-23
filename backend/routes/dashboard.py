from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from backend.database.mongodb import prediction_collection

import os

router = APIRouter(tags=["Dashboard"])

# Template Folder
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

templates = Jinja2Templates(
    directory=os.path.abspath(
        os.path.join(BASE_DIR, "..", "frontend", "templates")
    )
)


@router.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):

    user = request.session.get("user")

    if not user:
        return RedirectResponse("/", status_code=302)

    predictions = list(
        prediction_collection.find(
            {"email": user["email"]}
        ).sort("_id", -1)
    )

    total = len(predictions)

    healthy = 0
    diseased = 0

    disease_count = {}

    for item in predictions:

        disease = item.get("prediction", {}).get("disease", "Unknown")

        if disease.lower() == "healthy":
            healthy += 1
        else:
            diseased += 1

        disease_count[disease] = disease_count.get(disease, 0) + 1

    return templates.TemplateResponse(
        "dashboard.html",
        {
            "request": request,
            "user": user,
            "predictions": predictions[:10],
            "total": total,
            "healthy": healthy,
            "diseased": diseased,
            "disease_labels": list(disease_count.keys()),
            "disease_values": list(disease_count.values())
        }
    )