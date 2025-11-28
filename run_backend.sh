#!/bin/bash
# Script to setup and run the backend server

set -e

echo "🚀 Démarrage du backend Hotel Recommender..."

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 n'est pas installé"
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    echo "📦 Création de l'environnement virtuel..."
    python3 -m venv .venv
fi

# Activate virtual environment
echo "✅ Activation de l'environnement virtuel..."
source .venv/bin/activate

# Install requirements
echo "📥 Installation des dépendances..."
pip install --upgrade pip > /dev/null 2>&1
pip install -r backend/requirements.txt > /dev/null 2>&1

# Run the Flask app
echo ""
echo "=========================================="
echo "✨ Serveur lancé sur http://0.0.0.0:5000"
echo "=========================================="
echo ""
echo "Endpoints disponibles:"
echo "  - GET  http://localhost:5000/health"
echo "  - POST http://localhost:5000/recommendations"
echo ""
echo "Pour arrêter le serveur: CTRL+C"
echo "=========================================="
echo ""

cd backend/app
python -m flask.cli run --host=0.0.0.0 --port=5000
