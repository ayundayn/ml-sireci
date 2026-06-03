from pydantic import BaseModel
from typing import List

class ItineraryRequest(BaseModel):

    wisata_ids: List[int]
    kuliner_ids: List[int]

    total_hari: int = 1
    budget: int = 1000000
    start_time: str = "08:00"
    end_time: str = "20:00"
