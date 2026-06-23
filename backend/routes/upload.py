import os
import shutil
import uuid
from datetime import datetime

from fastapi import APIRouter, Request, UploadFile, File
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from backend.predict import predict_disease
from backend.database.mongodb import prediction_collection
from backend.utils.pdf_generator import generate_report
from backend.models.recommendation import recommendations

router = APIRouter()

# ------------------------------------------
# Templates
# ------------------------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

templates = Jinja2Templates(
    directory=os.path.abspath(
        os.path.join(BASE_DIR, "..", "frontend", "templates")
    )
)

# ------------------------------------------
# Upload Folder
# ------------------------------------------
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# ------------------------------------------
# Upload Page
# ------------------------------------------
@router.get("/upload", response_class=HTMLResponse)
async def upload_page(request: Request):

    user = request.session.get("user")

    if not user:
        return RedirectResponse("/", status_code=302)

    return templates.TemplateResponse(
        "upload.html",
        {
            "request": request,
            "user": user
        }
    )


# ------------------------------------------
# Upload Image & Predict Disease
# ------------------------------------------
@router.post("/upload")
async def upload_image(
    request: Request,
    file: UploadFile = File(...)
):

    user = request.session.get("user")

    if not user:
        return RedirectResponse("/", status_code=302)

    # Create folder by date
    today = datetime.now().strftime("%Y-%m-%d")
    daily_folder = os.path.join(UPLOAD_FOLDER, today)
    os.makedirs(daily_folder, exist_ok=True)

    # Unique filename
    extension = file.filename.split(".")[-1]
    filename = f"{uuid.uuid4()}.{extension}"

    filepath = os.path.join(daily_folder, filename)

    # Save uploaded image
    with open(filepath, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Predict disease
    result = predict_disease(filepath)

    # Recommendation
    recommendation = recommendations.get(
        result["disease"],
        {
            "description": "No information available.",
            "treatment": "-",
            "fertilizer": "-",
            "irrigation": "-",
            "precautions": "-"
        }
    )

    # Generate PDF
    generate_report(
        user,
        result,
        recommendation
    )

    # Save prediction in MongoDB
    prediction = {
        "name": user["name"],
        "email": user["email"],
        "image": filename,
        "prediction": result,
        "uploaded_at": datetime.now()
    }

    inserted = prediction_collection.insert_one(prediction)

    print("=" * 60)
    print("Prediction Saved Successfully")
    print("Inserted ID:", inserted.inserted_id)
    print(prediction)
    print("=" * 60)

    # Redirect to report page
    return RedirectResponse(
        url="/report",
        status_code=303
    )