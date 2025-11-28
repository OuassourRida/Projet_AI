# 🏨 Backend - Démarrage Rapide

## Prérequis
- **Python 3.8+** installé
- **Linux/Mac/Windows** avec bash/terminal

## Option 1 : Lancement Automatique (Recommandé)

```bash
cd /home/mouad/Projet_AI
bash run_backend.sh
```

Le script va automatiquement :
1. ✅ Créer un environnement virtuel `.venv`
2. ✅ Installer les dépendances (`flask`, `pandas`, etc.)
3. ✅ Lancer le serveur Flask sur `http://localhost:5000`

---

## Option 2 : Lancement Manuel

### Étape 1 : Créer l'environnement virtuel
```bash
cd /home/mouad/Projet_AI
python3 -m venv .venv
```

### Étape 2 : Activer l'environnement virtuel

**Sur Linux/Mac :**
```bash
source .venv/bin/activate
```

**Sur Windows :**
```bash
.venv\Scripts\activate
```

### Étape 3 : Installer les dépendances
```bash
pip install -r backend/requirements.txt
```

### Étape 4 : Lancer le serveur
```bash
export FLASK_APP=backend/app/main.py
flask run --host=0.0.0.0 --port=5000
```

Ou directement :
```bash
python backend/app/main.py
```

---

## Vérification du Serveur

Une fois le serveur lancé, testez-le :

### Health Check
```bash
curl http://localhost:5000/health
```

Réponse attendue :
```json
{"status":"ok"}
```

### Teste de Recommandations
```bash
curl -X POST http://localhost:5000/recommendations \
  -H "Content-Type: application/json" \
  -d '{"hotels":["La Mamounia"], "top_k":5}'
```

Réponse attendue :
```json
{
  "recommendations": [
    {
      "id": "H009",
      "name": "Palais Namaskar",
      "category": "Luxe",
      "location": "Palmeraie",
      "price": "$$$",
      "stars": 5,
      "avg_rating": 4.85
    },
    ...
  ]
}
```

---

## Erreurs Courantes

### ❌ `ModuleNotFoundError: No module named 'flask'`
→ Assurez-vous que l'environnement virtuel est activé : `source .venv/bin/activate`

### ❌ `Port 5000 already in use`
→ Changez le port :
```bash
flask run --host=0.0.0.0 --port=5001
```

### ❌ `FileNotFoundError: data/hotels.csv`
→ Assurez-vous que vous êtes dans le répertoire `/home/mouad/Projet_AI`

---

## Intégration Frontend

Le frontend (React) communique avec ce backend via l'endpoint POST `/recommendations`.

**Configuration Frontend :**
- L'API appelle `http://localhost:5000/recommendations`
- Format requis : `{ "hotels": [...] }`
- Réponse : `{ "recommendations": [...] }`

Si le backend n'est pas accessible, le frontend utilise un fallback mock.

---

## Arrêter le Serveur
```
CTRL + C
```

---

**✨ À bientôt sur http://localhost:5000!**
