"""
Banshari Main Application Entrypoint
"""

import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from .api.routes import router as api_router

app = FastAPI(
    title="Banshari Automotive Metasearch",
    description="Global Automotive Spare Parts Metasearch Engine & Landed Cost Aggregator",
    version="1.0.1"
)

# Enable CORS for cross-origin or local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API Router
app.include_router(api_router)

# Mount Frontend Static Directory
static_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "frontend", "static")

if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")

    @app.get("/styles.css")
    def serve_styles():
        return FileResponse(os.path.join(static_dir, "styles.css"))

    @app.get("/catalog.js")
    def serve_catalog_js():
        return FileResponse(os.path.join(static_dir, "catalog.js"))

    @app.get("/app.js")
    def serve_app_js():
        return FileResponse(os.path.join(static_dir, "app.js"))

    @app.get("/")
    def serve_frontend():
        return FileResponse(os.path.join(static_dir, "index.html"))
