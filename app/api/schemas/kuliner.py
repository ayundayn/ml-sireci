from pydantic import BaseModel, Field
from typing import List, Optional


class KulinerRecommendRequest(BaseModel):
    user_id: int = Field(..., description="ID user", ge=1)
    kategori: List[str] = Field(
        default=["Tradisional", "Inovatif", "Budaya"],
        description="Filter kategori kuliner"
    )
    budget_min: float = Field(default=0, description="Budget minimum", ge=0)
    budget_max: float = Field(default=1000000, description="Budget maksimum", ge=0)
    rating_min: float = Field(default=3.0, description="Rating minimum", ge=0, le=5)
    top_n: int = Field(default=10, description="Jumlah rekomendasi", ge=1, le=50)


class KulinerItem(BaseModel):
    kuliner_id: Optional[int] = None
    nama_tempat: str
    kategori_kuliner_id: str
    jam_buka: str
    jam_tutup: str
    alamat: str
    lokasi_geo: str
    htm_min: float
    htm_max: float
    rating: float
    skor_rekomendasi: float


class KulinerRecommendResponse(BaseModel):
    success: bool
    message: str
    count: int
    data: List[KulinerItem]


class KulinerRateRequest(BaseModel):
    user_id: int = Field(..., ge=1)
    kuliner_id: int = Field(..., ge=1)
    rating: float = Field(..., ge=1, le=5)


class KulinerRateResponse(BaseModel):
    success: bool
    message: str
