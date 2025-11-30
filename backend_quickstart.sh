#!/bin/bash
# Quick start script for backend testing

set -e

cd /home/mouad/Projet_AI

echo "=========================================="
echo "🏨 Hotel Recommender Backend - Quick Start"
echo "=========================================="
echo ""

# Activate environment
source .venv/bin/activate

echo "✅ Environment activated"
echo ""

# Show available commands
echo "=========================================="
echo "📋 Available Commands:"
echo "=========================================="
echo ""
echo "1️⃣  Run the server:"
echo "   python backend/app/main.py"
echo ""
echo "2️⃣  Run tests:"
echo "   pytest tests/test_backend.py -v"
echo ""
echo "3️⃣  Test direct import:"
echo "   python test_backend.py"
echo ""
echo "4️⃣  Test with curl (in another terminal):"
echo "   curl http://localhost:5000/health"
echo "   curl -X POST http://localhost:5000/recommendations \\"
echo "     -H 'Content-Type: application/json' \\"
echo "     -d '{\"hotels\":[\"La Mamounia\"], \"top_k\":5}'"
echo ""
echo "=========================================="
echo "✨ Ready to start! Choose an option above."
echo "=========================================="
