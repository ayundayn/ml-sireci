from fastapi import APIRouter, HTTPException

from app.api.schemas.itinerary import (
    ItineraryRequest
)

from app.core.data_loader import DataLoader
from app.recommenders.itinerary_engine import ItineraryEngine

router = APIRouter()

data_loader = DataLoader()
engine = None


def get_engine():
    global engine

    if engine is None:
        engine = ItineraryEngine(data_loader)

    return engine


@router.post("/itinerary")
def generate_itinerary(req: ItineraryRequest):

    try:
        result = get_engine().generate(
            wisata_ids=req.wisata_ids,
            kuliner_ids=req.kuliner_ids,
            total_hari=req.total_hari,
            budget=req.budget,
            start_time=req.start_time,
            end_time=req.end_time
        )
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Error generating itinerary: {exc}"
        )

    return {
        "success": True,
        "data": result
    }
