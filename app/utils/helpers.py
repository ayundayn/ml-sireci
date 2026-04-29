import os
from typing import Any
import joblib
import pandas as pd
from app.config import settings


def save_model(model: Any, filename: str) -> str:
    """Save model to artifacts/models"""
    os.makedirs(settings.models_dir, exist_ok=True)
    path = os.path.join(settings.models_dir, filename)
    joblib.dump(model, path)
    return path


def load_model(filename: str) -> Any:
    """Load model from artifacts/models"""
    path = os.path.join(settings.models_dir, filename)
    if not os.path.exists(path):
        raise FileNotFoundError(f"Model not found: {path}")
    return joblib.load(path)


def calculate_recommendation_score(rating: float, max_rating: float) -> float:
    """Calculate normalized recommendation score"""
    if max_rating == 0:
        return 0.0
    return round(rating / max_rating, 2)


def format_price_range(min_price: float, max_price: float) -> str:
    """Format price range for display"""
    if min_price == 0 and max_price == 0:
        return "Gratis"
    return f"Rp {min_price:,.0f} - Rp {max_price:,.0f}"
