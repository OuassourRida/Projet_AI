#!/bin/bash
# Backend standalone launcher - no frontend integration

set -e

echo "🏨 Lancement du Backend Hotel Recommender (Standalone)"
echo "========================================================"

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 n'est pas installé"
    exit 1
fi

# Setup venv if needed
if [ ! -d ".venv" ]; then
    echo "📦 Création de l'environnement virtuel..."
    python3 -m venv .venv
fi

# Activate venv
source .venv/bin/activate

# Install dependencies
echo "📥 Installation des dépendances..."
pip install -q --upgrade pip
pip install -q -r backend/requirements.txt

echo ""
echo "✅ Environnement prêt"
echo ""
echo "=========================================="
echo "🚀 Serveur lancé sur http://localhost:5000"
echo "=========================================="
echo ""
echo "Endpoints:"
echo "  GET  /health"
echo "  POST /recommendations"
echo ""
echo "Test rapide:"
echo "  curl http://localhost:5000/health"
echo ""
echo "Pour arrêter: CTRL+C"
echo "=========================================="
echo ""

cd backend/app
export FLASK_ENV=production
python -c "from main import app; app.run(host='0.0.0.0', port=5000, debug=False)"
