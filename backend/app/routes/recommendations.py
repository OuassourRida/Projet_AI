"""
Routes API pour les recommandations d'hôtels
Endpoints pour récupérer les hôtels et générer des recommandations personnalisées
"""

from fastapi import APIRouter, HTTPException, Body
from typing import Dict, List, Any
from pydantic import BaseModel
import logging

from ..models.knn_recommender import HotelRecommender

# Configuration du logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Créer le router FastAPI
router = APIRouter()

# Instance globale du recommender
recommender = HotelRecommender()

# Modèles Pydantic pour la validation des données
class UserRatings(BaseModel):
    """Modèle pour les ratings utilisateur"""
    ratings: Dict[str, float]
    
    class Config:
        json_schema_extra = {
            "example": {
                "ratings": {
                    1: 4.5,
                    2: 3.0,
                    5: 5.0
                }
            }
        }

class RecommendationRequest(BaseModel):
    """Modèle pour une demande de recommandation"""
    user_ratings: Dict[str, float]
    n_recommendations: int = 5
    
    class Config:
        json_schema_extra = {
            "example": {
                "user_ratings": {
                    1: 4.5,
                    2: 3.0,
                    5: 5.0,
                    8: 4.0
                },
                "n_recommendations": 5
            }
        }

class HotelResponse(BaseModel):
    """Modèle pour la réponse d'un hôtel"""
    hotel_id: str
    nom: str
    categorie: str
    localisation: str
    prix: str
    commodites: str
    description: str = ""
    avg_rating: float

class RecommendationResponse(BaseModel):
    """Modèle pour une recommandation"""
    hotel_id: str
    nom: str
    predicted_rating: float
    categorie: str
    localisation: str
    prix: str
    commodites: str
    explanation: str


@router.get("/hotels", response_model=List[HotelResponse])
async def get_all_hotels():
    """
    Récupère tous les hôtels disponibles
    
    Returns:
        List[HotelResponse]: Liste de tous les hôtels avec leurs détails
    """
    try:
        logger.info("Récupération de tous les hôtels")
        hotels = recommender.get_all_hotels()
        
        if not hotels:
            logger.warning("Aucun hôtel trouvé")
            return []
        
        logger.info(f"Retour de {len(hotels)} hôtels")
        return hotels
        
    except Exception as e:
        logger.error(f"Erreur lors de la récupération des hôtels: {e}")
        raise HTTPException(
            status_code=500, 
            detail="Erreur interne lors de la récupération des hôtels"
        )


@router.get("/hotels/{hotel_id}", response_model=HotelResponse)
async def get_hotel_by_id(hotel_id: int):
    """
    Récupère un hôtel spécifique par son ID
    
    Args:
        hotel_id (int): ID de l'hôtel
        
    Returns:
        HotelResponse: Détails de l'hôtel
    """
    try:
        logger.info(f"Récupération de l'hôtel {hotel_id}")
        hotels = recommender.get_all_hotels()
        
        # Rechercher l'hôtel par ID
        hotel = next((h for h in hotels if h['hotel_id'] == hotel_id), None)
        
        if not hotel:
            logger.warning(f"Hôtel {hotel_id} non trouvé")
            raise HTTPException(status_code=404, detail="Hôtel non trouvé")
            
        logger.info(f"Hôtel {hotel_id} trouvé: {hotel['nom']}")
        return hotel
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erreur lors de la récupération de l'hôtel {hotel_id}: {e}")
        raise HTTPException(
            status_code=500, 
            detail="Erreur interne lors de la récupération de l'hôtel"
        )


@router.post("/recommend", response_model=List[RecommendationResponse])
async def get_recommendations(request: RecommendationRequest):
    """
    Génère des recommandations personnalisées d'hôtels
    
    Args:
        request (RecommendationRequest): Ratings utilisateur et nombre de recommandations
        
    Returns:
        List[RecommendationResponse]: Liste des recommandations personnalisées
    """
    try:
        logger.info(f"Génération de recommandations pour {len(request.user_ratings)} ratings")
        
        # Validation des ratings
        if not request.user_ratings:
            raise HTTPException(
                status_code=400, 
                detail="Au moins un rating d'hôtel est requis pour générer des recommandations"
            )
            
        # Valider que les ratings sont dans la bonne plage
        for hotel_id, rating in request.user_ratings.items():
            if not 1 <= rating <= 5:
                raise HTTPException(
                    status_code=400,
                    detail=f"Le rating pour l'hôtel {hotel_id} doit être entre 1 et 5"
                )
        
        # Générer les recommandations
        recommendations = recommender.get_recommendations(
            user_ratings=request.user_ratings,
            n_recommendations=request.n_recommendations
        )
        
        if not recommendations:
            logger.warning("Aucune recommandation générée")
            return []
        
        logger.info(f"Génération de {len(recommendations)} recommandations réussie")
        return recommendations
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erreur lors de la génération des recommandations: {e}")
        raise HTTPException(
            status_code=500,
            detail="Erreur interne lors de la génération des recommandations"
        )


@router.post("/recommend/simple")
async def get_simple_recommendations(user_ratings: Dict[int, float] = Body(...)):
    """
    Version simplifiée de l'endpoint de recommandations
    Accepte directement un dictionnaire de ratings
    
    Args:
        user_ratings (Dict[int, float]): Ratings utilisateur {hotel_id: rating}
        
    Returns:
        dict: Recommandations avec métadonnées
    """
    try:
        logger.info(f"Génération de recommandations simples pour {len(user_ratings)} ratings")
        
        if not user_ratings:
            raise HTTPException(
                status_code=400, 
                detail="Au moins un rating d'hôtel est requis"
            )
        
        # Générer les recommandations (par défaut 5)
        recommendations = recommender.get_recommendations(
            user_ratings=user_ratings,
            n_recommendations=5
        )
        
        # Retourner avec métadonnées
        return {
            "recommendations": recommendations,
            "total_recommendations": len(recommendations),
            "user_ratings_count": len(user_ratings),
            "algorithm": "KNN Collaborative Filtering",
            "similarity_metric": "Cosine Similarity"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erreur lors des recommandations simples: {e}")
        raise HTTPException(
            status_code=500,
            detail="Erreur lors de la génération des recommandations"
        )


@router.get("/stats")
async def get_system_stats():
    """
    Récupère les statistiques du système de recommandation
    
    Returns:
        dict: Statistiques générales
    """
    try:
        logger.info("Récupération des statistiques système")
        
        # S'assurer que les données sont chargées
        if not recommender._data_loaded:
            recommender.load_data()
        
        # Calculer les statistiques
        total_hotels = len(recommender.hotels_df)
        total_users = len(recommender.users_df) 
        total_ratings = len(recommender.ratings_df)
        
        # Statistiques des ratings
        avg_rating = recommender.ratings_df['rating'].mean()
        min_rating = recommender.ratings_df['rating'].min()
        max_rating = recommender.ratings_df['rating'].max()
        
        # Statistiques des hôtels
        categories = recommender.hotels_df['categorie'].value_counts().to_dict()
        locations = recommender.hotels_df['localisation'].value_counts().to_dict()
        
        stats = {
            "total_hotels": total_hotels,
            "total_users": total_users,
            "total_ratings": total_ratings,
            "rating_stats": {
                "average": round(avg_rating, 2),
                "min": min_rating,
                "max": max_rating
            },
            "hotel_categories": categories,
            "hotel_locations": locations,
            "system_info": {
                "algorithm": "KNN Collaborative Filtering",
                "similarity_metric": "Cosine Similarity",
                "k_neighbors": recommender.k
            }
        }
        
        logger.info("Statistiques système récupérées avec succès")
        return stats
        
    except Exception as e:
        logger.error(f"Erreur lors de la récupération des statistiques: {e}")
        raise HTTPException(
            status_code=500,
            detail="Erreur lors de la récupération des statistiques"
        )


@router.get("/health")
async def health_check():
    """
    Vérifie l'état de santé de l'API
    
    Returns:
        dict: Status de l'API
    """
    try:
        # Vérifier que le recommender peut charger les données
        if not recommender._data_loaded:
            recommender.load_data()
            
        return {
            "status": "healthy",
            "message": "API de recommandation d'hôtels opérationnelle",
            "data_loaded": recommender._data_loaded,
            "version": "1.0.0"
        }
        
    except Exception as e:
        logger.error(f"Erreur de santé de l'API: {e}")
        return {
            "status": "unhealthy",
            "message": "Erreur lors de la vérification de santé",
            "error": str(e)
        }
