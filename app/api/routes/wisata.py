from fastapi import APIRouter, HTTPException
from typing import List
import pandas as pd
import numpy as np

from app.api.schemas.wisata import (
    WisataRecommendRequest,
    WisataRecommendResponse,
    WisataRateRequest,
    WisataRateResponse
)
from app.core.data_loader import DataLoader
from app.recommenders.wisata_recommender import WisataRecommender

router = APIRouter(prefix="/api/v1/wisata", tags=["wisata"])

# Global instances
data_loader = DataLoader()
wisata_recommender = WisataRecommender()
sample_ratings = None


def initialize_service():
    """Initialize the recommender service"""
    global sample_ratings

    try:
        # Load data
        df = data_loader.load_wisata()
        wisata_recommender.load_data(df)

        # Load ratings from database
        sample_ratings = data_loader.load_ratings_wisata()

        # Fallback: generate sample ratings if no ratings in DB
        if len(sample_ratings) == 0:
            sample_ratings = pd.DataFrame({
                'user_id': np.random.randint(1, 15, 80),
                'wisata': np.random.choice(df['nama_tempat'].tolist(), 80),
                'rating': np.random.randint(3, 6, 80)
            })

        # Build CF matrix
        wisata_recommender.build_user_item_matrix(sample_ratings)

        return True
    except Exception as e:
        print(f"Error initializing service: {e}")
        return False


@router.post("/recommend", response_model=WisataRecommendResponse)
async def recommend_wisata(request: WisataRecommendRequest):
    """Get rekomendasi wisata menggunakan hybrid filtering"""

    sample_ratings = data_loader.load_ratings_wisata()

    wisata_recommender.build_user_item_matrix(
        sample_ratings
    )
    
    try:
        # Get hybrid recommendations
        result_df = wisata_recommender.recommend_hybrid(
            user_id=request.user_id,
            kategori=request.kategori,
            budget_min=request.budget_min,
            budget_max=request.budget_max,
            rating_min=request.rating_min,
            top_n=request.top_n
        )

        if result_df.empty:
            return WisataRecommendResponse(
                success=True,
                message="Tidak ada rekomendasi ditemukan",
                count=0,
                data=[]
            )

        # Convert to response format
        items = []
        for _, row in result_df.iterrows():
            items.append({
                "wisata_id": row.get('wisata_id'),
                "nama_tempat": row['nama_tempat'],
                "kategori": row.get('kategori'),
                "jam_buka": str(row['jam_buka']),
                "jam_tutup": str(row['jam_tutup']),
                "alamat": row['alamat'],
                "lokasi_geo": row['lokasi_geo'],
                "htm_min_domestik": float(row['htm_min_domestik']),
                "htm_max_domestik": float(row['htm_max_domestik']),
                "htm_min_mancanegara": float(row['htm_min_mancanegara']),
                "htm_max_mancanegara": float(row['htm_max_mancanegara']),
                "akses_transportasi": row['akses_transportasi'],
                "rating": float(row['rating']),
                "skor_rekomendasi": float(row.get('skor_rekomendasi', 0.0))
            })

        return WisataRecommendResponse(
            success=True,
            message=f"Ditemukan {len(items)} rekomendasi",
            count=len(items),
            data=items
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error generating recommendations: {str(e)}"
        )


@router.post("/rate", response_model=WisataRateResponse)
async def rate_wisata(request: WisataRateRequest):
    """Submit rating untuk wisata"""

    # TODO: Simpan rating ke database
    # Untuk sekarang hanya return success

    return WisataRateResponse(
        success=True,
        message=f"Rating {request.rating} untuk wisata {request.wisata_id} berhasil disimpan"
    )


@router.get("/popular")
async def get_popular_wisata(limit: int = 10):
    """Get wisata paling populer berdasarkan rating"""

    try:
        df = data_loader.load_wisata()
        popular = df.nlargest(limit, 'rating')

        return {
            "success": True,
            "count": len(popular),
            "data": popular.to_dict(orient='records')
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error getting popular items: {str(e)}"
        )
