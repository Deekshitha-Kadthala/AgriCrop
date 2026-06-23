import os

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware

# -----------------------------
# Import Routers
# -----------------------------
from backend.routes.auth import router as auth_router
from backend.routes.dashboard import router as dashboard_router
from backend.routes.upload import router as upload_router
from backend.routes.moisture import router as moisture_router
from backend.routes.report import router as report_router
from backend.routes.map import router as map_router
from backend.routes.admin import router as admin_router

# -----------------------------
# Create FastAPI App
# -----------------------------
app = FastAPI(
    title="AgriCrop - AI Plant Disease Detection",
    description="AI-based Crop Disease Detection and Soil Moisture Prediction System",
    version="1.0.0"
)

# -----------------------------
# Session Middleware
# -----------------------------
app.add_middleware(
    SessionMiddleware,
    secret_key="agricrop_super_secret_key_2026"
)

# -----------------------------
# Project Paths
# -----------------------------
# backend folder
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# AgriCrop folder
PROJECT_DIR = os.path.abspath(os.path.join(BASE_DIR, ".."))

STATIC_DIR = os.path.join(PROJECT_DIR, "frontend", "static")

print("=" * 60)
print("Backend Folder :", BASE_DIR)
print("Project Folder :", PROJECT_DIR)
print("Static Folder  :", STATIC_DIR)
print("Static Exists? :", os.path.exists(STATIC_DIR))
print("=" * 60)

# -----------------------------
# Mount Static Folder
# -----------------------------
if not os.path.exists(STATIC_DIR):
    raise RuntimeError(f"Static folder not found:\n{STATIC_DIR}")

app.mount(
    "/static",
    StaticFiles(directory=STATIC_DIR),
    name="static"
)

# -----------------------------
# Include Routers
# -----------------------------
app.include_router(auth_router)
app.include_router(dashboard_router)
app.include_router(upload_router)
app.include_router(moisture_router)
app.include_router(report_router)
app.include_router(map_router)
app.include_router(admin_router)

# -----------------------------
# Startup
# -----------------------------
@app.on_event("startup")
async def startup_event():
    print("=" * 60)
    print("🌿 AgriCrop Server Started Successfully")
    print("🚀 FastAPI Running...")
    print("=" * 60)

# -----------------------------
# Shutdown
# -----------------------------
@app.on_event("shutdown")
async def shutdown_event():
    print("🛑 AgriCrop Server Stopped")

# -----------------------------
# Health Check
# -----------------------------
@app.get("/health")
async def health():
    return {
        "status": "OK",
        "message": "AgriCrop Backend Running Successfully"
    }