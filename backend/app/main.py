"""
Application principale FastAPI pour le système de recommandation d'hôtels
Serveur API avec CORS activé pour l'interface React
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
import logging
from contextlib import asynccontextmanager

from .routes.recommendations import router as recommendations_router
from .models.knn_recommender import HotelRecommender

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Instance globale du recommender
recommender = HotelRecommender()

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Gestionnaire du cycle de vie de l'application
    Initialise le modèle au démarrage et nettoie à l'arrêt
    """
    # Démarrage
    try:
        logger.info("Initialisation du système de recommandation...")
        recommender.load_data()
        logger.info("✅ Système de recommandation initialisé avec succès")
        
    except Exception as e:
        logger.error(f"❌ Erreur lors de l'initialisation: {e}")
        
    yield  # L'application fonctionne ici
    
    # Arrêt
    logger.info("Arrêt du système de recommandation")

# Créer l'application FastAPI
app = FastAPI(
    title="API Système de Recommandation d'Hôtels - Marrakech",
    description="""
    API REST pour un système de recommandation d'hôtels à Marrakech.
    
    Utilise le filtrage collaboratif avec l'algorithme KNN et la similarité cosinus
    pour recommander des hôtels personnalisés basés sur les préférences des utilisateurs.
    
    ## Fonctionnalités
    
    * **GET /hotels** - Récupérer tous les hôtels disponibles
    * **GET /hotels/{hotel_id}** - Détails d'un hôtel spécifique  
    * **POST /recommend** - Générer des recommandations personnalisées
    * **GET /stats** - Statistiques du système
    * **GET /health** - Vérification de santé de l'API
    
    ## Algorithme
    
    - **Filtrage collaboratif** avec KNN (k=5)
    - **Similarité cosinus** entre utilisateurs
    - **Gestion cold-start** avec recommandations populaires
    - **Prédictions** basées sur la moyenne pondérée des k plus proches voisins
    """,
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# Configuration CORS pour permettre les requêtes depuis React
app.add_middleware(
    CORSMiddleware,
    allow_origins=[],
    allow_origin_regex=r"http://(localhost|127\.0\.0\.1):\d+",
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# Inclure les routes
app.include_router(
    recommendations_router, 
    prefix="/api",
    tags=["Recommandations"]
)

# Route racine
@app.get("/", tags=["Root"])
async def root():
    """
    Page d'accueil de l'API
    
    Returns:
        dict: Informations de base sur l'API
    """
    return {
        "message": "API Système de Recommandation d'Hôtels - Marrakech",
        "version": "1.0.0",
        "algorithm": "KNN Collaborative Filtering",
        "similarity": "Cosine Similarity",
        "docs": "/docs",
        "health": "/api/health",
        "hotels": "/api/hotels",
        "recommend": "/api/recommend"
    }

# Gestionnaire d'erreurs global
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """
    Gestionnaire global des exceptions
    
    Args:
        request: Requête HTTP
        exc: Exception capturée
        
    Returns:
        JSONResponse: Réponse d'erreur formatée
    """
    logger.error(f"Erreur non gérée: {exc}")
    return JSONResponse(
        status_code=500,
        content={
            "error": "Erreur interne du serveur",
            "detail": "Une erreur inattendue s'est produite",
            "type": type(exc).__name__
        }
    )

# Point d'entrée pour le développement local
if __name__ == "__main__":
    logger.info("Démarrage du serveur de développement...")
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )