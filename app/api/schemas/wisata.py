from pydantic import BaseModel, Field
from typing import List, Optional


class WisataRecommendRequest(BaseModel):
    user_id: int = Field(..., description="ID user", ge=1)
    kategori: List[str] = Field(
        default=["Wisata Alam", "Wisata Budaya", "Wisata Edukasi", "Wisata Religi", "Wisata Belanja"],
        description="Filter kategori wisata"
    )
    budget_min: float = Field(default=0, description="Budget minimum", ge=0)
    budget_max: float = Field(default=1000000, description="Budget maksimum", ge=0)
    rating_min: float = Field(default=3.0, description="Rating minimum", ge=0, le=5)
    top_n: int = Field(default=10, description="Jumlah rekomendasi", ge=1, le=50)


class WisataItem(BaseModel):
    wisata_id: Optional[int] = None
    nama_tempat: str
    kategori: Optional[str] = None
    jam_buka: str
    jam_tutup: str
    alamat: str
    lokasi_geo: str
    htm_min_domestik: float
    htm_max_domestik: float
    htm_min_mancanegara: float
    htm_max_mancanegara: float
    akses_transportasi: str
    rating: float
    skor_rekomendasi: float


class WisataRecommendResponse(BaseModel):
    success: bool
    message: str
    count: int
    data: List[WisataItem]


class WisataRateRequest(BaseModel):
    user_id: int = Field(..., ge=1)
    wisata_id: int = Field(..., ge=1)
    rating: float = Field(..., ge=1, le=5)


class WisataRateResponse(BaseModel):
    success: bool
    message: str
