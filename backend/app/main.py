from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import os
from app.routes import recommendations


app = FastAPI(
    title="Hotel Recommendation API",
    description="API de recommandation d'hôtels à Marrakech",
    version="1.0.0"
)
app.include_router(recommendations.router, prefix="/recommend")

# CORS pour React
app.add_middleware(
    CORSMiddleware,
    # Allow localhost and 127.0.0.1 on any port during local development
    allow_origin_regex=r"http://localhost(:[0-9]+)?|http://127\.0\.0\.1(:[0-9]+)?",
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)

# Charger les données
def load_data():
    # Calcule le chemin vers <project_root>/data indépendamment du cwd
    try:
        from pathlib import Path
        project_root = Path(__file__).resolve().parents[2]
        data_dir = project_root / 'data'
        hotels_df = pd.read_csv(data_dir / 'hotels.csv')
        return hotels_df
    except Exception as e:
        print(f"Erreur lors du chargement des hotels.csv: {e}")
        return None

hotels_df = load_data()

@app.get("/")
async def root():
    return {"message": "🏨 API Recommandation Hôtels Marrakech"}

@app.get("/hotels")
async def get_hotels():
    if hotels_df is not None:
        return hotels_df.to_dict(orient="records")
    else:
        return {"error": "Données non chargées"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)