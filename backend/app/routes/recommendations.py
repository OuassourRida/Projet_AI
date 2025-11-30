from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Optional
from pathlib import Path
import pandas as pd

from app.models.knn_recommender import HotelRecommender

router = APIRouter()


class RatingItem(BaseModel):
    hotel_id: str
    rating: float


class RecommendationRequest(BaseModel):
    user_ratings: List[RatingItem]
    user_id: Optional[str] = None


# Load datasets once and initialize recommender
_RECOMMENDER: Optional[HotelRecommender] = None

def _init_recommender():
    global _RECOMMENDER
    if _RECOMMENDER is not None:
        return _RECOMMENDER

    project_root = Path(__file__).resolve().parents[3]
    data_dir = project_root / 'data'
    try:
        hotels_df = pd.read_csv(data_dir / 'hotels.csv')
        users_df = pd.read_csv(data_dir / 'users.csv')
        ratings_df = pd.read_csv(data_dir / 'ratings.csv')
    except Exception as e:
        raise RuntimeError(f"Impossible de charger les données depuis {data_dir}: {e}")

    _RECOMMENDER = HotelRecommender(hotels_df=hotels_df, ratings_df=ratings_df, k=5)
    return _RECOMMENDER


@router.post("/")
async def get_recommendations(request: RecommendationRequest):
    try:
        recommender = _init_recommender()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    # Convert Pydantic items to simple dicts
    ratings = [{"hotel_id": it.hotel_id, "rating": it.rating} for it in request.user_ratings]

    if len(ratings) == 0:
        raise HTTPException(status_code=400, detail="Veuillez fournir au moins une note dans 'user_ratings'.")

    try:
        recs = recommender.recommend(ratings, n_recommendations=5)
        return {"recommendations": recs}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur interne: {e}")