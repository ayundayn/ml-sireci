from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.api.routes import health, kuliner, wisata
from app.api.routes import itinerary

app = FastAPI(
    title="Banyu Guide ML Service",
    description="Recommendation API untuk wisata dan kuliner Banyuwangi",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(
    itinerary.router,
    prefix="/api",
    tags=["Itinerary"]
)

@app.get("/")
async def root():
    return {
        "service": "Banyu Guide ML Service",
        "version": "1.0.0",
        "status": "running",
        "docs": "/docs"
    }


@app.on_event("startup")
async def startup_event():
    """Initialize services on startup"""
    kuliner.initialize_service()
    wisata.initialize_service()


# Include routers
app.include_router(health.router)
app.include_router(kuliner.router)
app.include_router(wisata.router)
