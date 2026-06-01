from fastapi import APIRouter

from app.api.schemas.itinerary import (
    ItineraryRequest
)

from app.core.data_loader import DataLoader
from app.recommenders.itinerary_engine import ItineraryEngine

router = APIRouter()

data_loader = DataLoader()
engine = ItineraryEngine(data_loader)


@router.post("/itinerary")
def generate_itinerary(req: ItineraryRequest):

    result = engine.generate(
        wisata_ids=req.wisata_ids,
        kuliner_ids=req.kuliner_ids,
        total_hari=req.total_hari,
        budget=req.budget
    )

    return {
        "success": True,
        "data": result
    }