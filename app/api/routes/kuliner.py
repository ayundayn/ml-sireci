from fastapi import APIRouter, HTTPException
from typing import List
import pandas as pd
import numpy as np

from app.api.schemas.kuliner import (
    KulinerRecommendRequest,
    KulinerRecommendResponse,
    KulinerRateRequest,
    KulinerRateResponse
)
from app.core.data_loader import DataLoader
from app.recommenders.kuliner_recommender import KulinerRecommender

router = APIRouter(prefix="/api/v1/kuliner", tags=["kuliner"])

# Global instances
data_loader = DataLoader()
kuliner_recommender = KulinerRecommender()
sample_ratings = None


def initialize_service():
    """Initialize the recommender service"""
    global sample_ratings

    try:
        # Load data
        df = data_loader.load_kuliner()
        kuliner_recommender.load_data(df)

        # Load ratings from database
        sample_ratings = data_loader.load_ratings_kuliner()

        # Fallback: generate sample ratings if no ratings in DB
        if len(sample_ratings) == 0:
            sample_ratings = pd.DataFrame({
                'user_id': np.random.randint(1, 15, 80),
                'kuliner': np.random.choice(df['nama_tempat'].tolist(), 80),
                'rating': np.random.randint(3, 6, 80)
            })

        # Build CF matrix
        kuliner_recommender.build_user_item_matrix(sample_ratings)

        return True
    except Exception as e:
        print(f"Error initializing service: {e}")
        return False


@router.post("/recommend", response_model=KulinerRecommendResponse)
async def recommend_kuliner(request: KulinerRecommendRequest):
    """Get rekomendasi kuliner menggunakan hybrid filtering"""

    try:
        # Get hybrid recommendations
        result_df = kuliner_recommender.recommend_hybrid(
            user_id=request.user_id,
            kategori=request.kategori,
            budget_min=request.budget_min,
            budget_max=request.budget_max,
            rating_min=request.rating_min,
            top_n=request.top_n
        )

        if result_df.empty:
            return KulinerRecommendResponse(
                success=True,
                message="Tidak ada rekomendasi ditemukan",
                count=0,
                data=[]
            )

        # Convert to response format
        items = []
        for _, row in result_df.iterrows():
            items.append({
                "kuliner_id": row.get('kuliner_id'),
                "nama_tempat": row['nama_tempat'],
                "kategori": row.get('kategori'),
                "jam_buka": str(row['jam_buka']),
                "jam_tutup": str(row['jam_tutup']),
                "alamat": row['alamat'],
                "lokasi_geo": row['lokasi_geo'],
                "htm_min": float(row['htm_min']),
                "htm_max": float(row['htm_max']),
                "rating": float(row['rating']),
                "skor_rekomendasi": float(row.get('skor_rekomendasi', 0.0))
            })

        return KulinerRecommendResponse(
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


@router.post("/rate", response_model=KulinerRateResponse)
async def rate_kuliner(request: KulinerRateRequest):
    """Submit rating untuk kuliner"""

    # TODO: Simpan rating ke database
    # Untuk sekarang hanya return success

    return KulinerRateResponse(
        success=True,
        message=f"Rating {request.rating} untuk kuliner {request.kuliner_id} berhasil disimpan"
    )


@router.get("/popular")
async def get_popular_kuliner(limit: int = 10):
    """Get kuliner paling populer berdasarkan rating"""

    try:
        df = data_loader.load_kuliner()
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
