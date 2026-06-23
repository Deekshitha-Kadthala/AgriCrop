import os

from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from backend.database.mongodb import users_collection
from backend.utils.security import hash_password, verify_password

router = APIRouter(tags=["Authentication"])

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

TEMPLATE_DIR = os.path.abspath(
    os.path.join(BASE_DIR, "..", "frontend", "templates")
)

print("Template Folder =", TEMPLATE_DIR)

templates = Jinja2Templates(directory=TEMPLATE_DIR)


# -------------------------------------------------------
# Login Page
# -------------------------------------------------------

@router.get("/", response_class=HTMLResponse)
async def login_page(request: Request):

    if request.session.get("user"):
        return RedirectResponse(url="/dashboard", status_code=302)

    return templates.TemplateResponse(
        request=request,
        name="login.html",
        context={
            "message": ""
        }
    )


# -------------------------------------------------------
# Register Page
# -------------------------------------------------------

@router.get("/register", response_class=HTMLResponse)
async def register_page(request: Request):

    if request.session.get("user"):
        return RedirectResponse(url="/dashboard", status_code=302)

    return templates.TemplateResponse(
        request=request,
        name="register.html",
        context={
            "message": ""
        }
    )


# -------------------------------------------------------
# Register User
# -------------------------------------------------------

@router.post("/register")
async def register_user(
    request: Request,
    name: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    confirm_password: str = Form(...)
):

    name = str(name).strip()
    email = str(email).strip().lower()
    password = str(password).strip()
    confirm_password = str(confirm_password).strip()

    if not name or not email or not password or not confirm_password:
        return templates.TemplateResponse(
            request=request,
            name="register.html",
            context={
                "message": "All fields are required."
            }
        )

    if password != confirm_password:
        return templates.TemplateResponse(
            request=request,
            name="register.html",
            context={
                "message": "Passwords do not match."
            }
        )

    print("=" * 60)
    print("REGISTER DEBUG")
    print("Name:", name)
    print("Email:", email)
    print("Password:", repr(password))
    print("Password Length:", len(password))
    print("=" * 60)

    existing_user = users_collection.find_one(
        {"email": email}
    )

    if existing_user:
        return templates.TemplateResponse(
            request=request,
            name="register.html",
            context={
                "message": "Email already registered."
            }
        )

    try:
        hashed_password = hash_password(password)

        users_collection.insert_one({
            "name": name,
            "email": email,
            "password": hashed_password
        })

    except Exception as e:
        print("Registration Error:", e)

        return templates.TemplateResponse(
            request=request,
            name="register.html",
            context={
                "message": f"Registration Error: {str(e)}"
            }
        )

    return RedirectResponse(
        url="/",
        status_code=302
    )


# -------------------------------------------------------
# Login User
# -------------------------------------------------------

@router.post("/login")
async def login_user(
    request: Request,
    email: str = Form(...),
    password: str = Form(...)
):

    email = str(email).strip().lower()
    password = str(password).strip()

    user = users_collection.find_one(
        {"email": email}
    )

    if user is None:
        return templates.TemplateResponse(
            request=request,
            name="login.html",
            context={
                "message": "Invalid email or password."
            }
        )

    if not verify_password(password, user["password"]):
        return templates.TemplateResponse(
            request=request,
            name="login.html",
            context={
                "message": "Invalid email or password."
            }
        )

    request.session["user"] = {
        "name": user["name"],
        "email": user["email"]
    }

    return RedirectResponse(
        url="/dashboard",
        status_code=302
    )


# -------------------------------------------------------
# Logout
# -------------------------------------------------------

@router.get("/logout")
async def logout(request: Request):

    request.session.clear()

    return RedirectResponse(
        url="/",
        status_code=302
    )