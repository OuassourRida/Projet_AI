# utils/data_generator.py - VERSION FINALE CORRIGÉE
import pandas as pd
import numpy as np
import random
import os
from datetime import datetime, timedelta

print("🚀 DÉMARRAGE du générateur de données...")

try:
    from faker import Faker
    print("✅ Faker importé avec succès")
except ImportError as e:
    print(f"❌ Erreur import Faker: {e}")
    exit(1)

class DataGenerator:
    def __init__(self, seed=42):
        print("📦 Initialisation du générateur...")
        self.fake = Faker()
        np.random.seed(seed)
        random.seed(seed)
        print("✅ Générateur initialisé")
    
    def generer_hotels(self, n_hotels=80):
        """Génère un dataset réaliste d'hôtels à Marrakech - VERSION CORRIGÉE"""
        print(f"🏨 Génération de {n_hotels} hôtels...")
        
        categories = ['Luxe', 'Riad', 'Budget', 'Affaires', 'Boutique']
        localisations = ['Médina', 'Guéliz', 'Hivernage', 'Palmeraie', 'Kasbah']
        
        # Commodités par catégorie d'hôtel - CORRIGÉ avec plus d'éléments
        commodites_par_categorie = {
            'Luxe': ['Piscine', 'SPA', 'WiFi', 'Parking', 'Restaurant', 'Room Service', 'Gym', 'Bar', 'Concierge'],
            'Riad': ['Terrasse', 'Petit-déjeuner', 'WiFi', 'Jardin', 'Cuisine traditionnelle', 'Patio', 'Fontaine'],
            'Budget': ['WiFi', 'Parking', 'Petit-déjeuner', 'Climatisation', 'Salle de bain privée'],
            'Affaires': ['WiFi', 'Parking', 'Business Center', 'Petit-déjeuner', 'Salle de réunion', 'Service de nettoyage'],
            'Boutique': ['Piscine', 'WiFi', 'Design unique', 'Restaurant', 'Décoration artisanale', 'Jardin']
        }
        
        hotels = []
        
        # Hôtels réels célèbres de Marrakech
        hotels_celebrates = [
            {'nom': 'La Mamounia', 'categorie': 'Luxe', 'localisation': 'Médina', 'prix': '$$$'},
            {'nom': 'Royal Mansour', 'categorie': 'Luxe', 'localisation': 'Médina', 'prix': '$$$'},
            {'nom': 'Four Seasons', 'categorie': 'Luxe', 'localisation': 'Hivernage', 'prix': '$$$'},
            {'nom': 'Riad Kniza', 'categorie': 'Riad', 'localisation': 'Médina', 'prix': '$$'},
            {'nom': 'Ibis Marrakech', 'categorie': 'Budget', 'localisation': 'Guéliz', 'prix': '$'},
            {'nom': 'Sofitel Marrakech', 'categorie': 'Luxe', 'localisation': 'Palmeraie', 'prix': '$$$'},
            {'nom': 'Le Méridien', 'categorie': 'Affaires', 'localisation': 'Guéliz', 'prix': '$$'},
            {'nom': 'Riad El Fenn', 'categorie': 'Riad', 'localisation': 'Médina', 'prix': '$$'},
            {'nom': 'Palais Namaskar', 'categorie': 'Luxe', 'localisation': 'Palmeraie', 'prix': '$$$'},
            {'nom': 'Hotel Dar Anika', 'categorie': 'Riad', 'localisation': 'Médina', 'prix': '$$'},
        ]
        
        # Ajouter les hôtels célèbres
        for i, hotel in enumerate(hotels_celebrates):
            commodites_disponibles = commodites_par_categorie[hotel['categorie']]
            n_commodites = min(random.randint(2, 4), len(commodites_disponibles))  # CORRECTION ICI
            commodites = random.sample(commodites_disponibles, n_commodites)
            
            hotels.append({
                'hotel_id': f'H{i+1:03d}',
                'nom': hotel['nom'],
                'categorie': hotel['categorie'],
                'localisation': hotel['localisation'],
                'prix': hotel['prix'],
                'etoiles': 5 if hotel['categorie'] == 'Luxe' else random.randint(3, 4),
                'commodites': ', '.join(commodites)
            })
        
        # Générer les hôtels restants
        for i in range(len(hotels_celebrates), n_hotels):
            categorie = random.choice(categories)
            localisation = random.choice(localisations)
            
            # Prix cohérent avec la catégorie
            if categorie == 'Luxe':
                prix = '$$$'
                etoiles = 5
            elif categorie == 'Riad':
                prix = random.choice(['$$', '$$$'])
                etoiles = random.randint(4, 5)
            elif categorie == 'Budget':
                prix = '$'
                etoiles = random.randint(2, 3)
            else:  # Affaires ou Boutique
                prix = '$$'
                etoiles = random.randint(3, 4)
            
            commodites_disponibles = commodites_par_categorie[categorie]
            n_commodites = min(random.randint(2, 4), len(commodites_disponibles))  # CORRECTION ICI
            commodites = random.sample(commodites_disponibles, n_commodites)
            
            # Générer un nom réaliste
            if categorie == 'Riad':
                nom = f"Riad {self.fake.last_name()}"
            elif categorie == 'Luxe':
                nom = f"{self.fake.last_name()} Palace"
            else:
                nom = f"Hotel {self.fake.last_name()} {localisation}"
            
            hotels.append({
                'hotel_id': f'H{i+1:03d}',
                'nom': nom,
                'categorie': categorie,
                'localisation': localisation,
                'prix': prix,
                'etoiles': etoiles,
                'commodites': ', '.join(commodites)
            })
        
        print(f"✅ {len(hotels)} hôtels générés")
        return pd.DataFrame(hotels)
    
    def generer_utilisateurs(self, n_utilisateurs=2000):
        """Génère des utilisateurs réalistes avec profils"""
        print(f"👥 Génération de {n_utilisateurs} utilisateurs...")
        
        types_voyage = ['Romantique', 'Affaires', 'Familial', 'Solo', 'Groupe']
        budgets = ['Économique', 'Moyen', 'Luxe']
        
        utilisateurs = []
        
        for i in range(n_utilisateurs):
            age = random.randint(18, 70)
            
            # Le type de voyage dépend de l'âge
            if age < 25:
                type_voyage = random.choice(['Solo', 'Groupe'])
                budget = 'Économique'
            elif age < 40:
                type_voyage = random.choice(['Romantique', 'Affaires', 'Familial'])
                budget = random.choice(['Moyen', 'Luxe'])
            else:
                type_voyage = random.choice(['Romantique', 'Familial', 'Affaires'])
                budget = random.choice(['Moyen', 'Luxe'])
            
            utilisateurs.append({
                'user_id': f'U{i+1:04d}',
                'age': age,
                'type_voyage': type_voyage,
                'budget': budget,
                'nationalite': self.fake.country()
            })
        
        print(f"✅ {len(utilisateurs)} utilisateurs générés")
        return pd.DataFrame(utilisateurs)
    
    def generer_ratings(self, hotels_df, users_df, n_ratings=50000):
        """Génère des ratings réalistes basés sur les profils"""
        print(f"⭐ Génération de {n_ratings} ratings...")
        
        ratings = []
        hotel_ids = hotels_df['hotel_id'].tolist()
        user_ids = users_df['user_id'].tolist()
        
        # Pré-calculer les préférences par type d'utilisateur
        preferences_par_type = {
            'Romantique': {'Luxe': 4.5, 'Riad': 4.7, 'Budget': 2.5, 'Affaires': 3.0, 'Boutique': 4.3},
            'Affaires': {'Luxe': 4.2, 'Riad': 3.5, 'Budget': 3.8, 'Affaires': 4.5, 'Boutique': 3.7},
            'Familial': {'Luxe': 4.3, 'Riad': 4.0, 'Budget': 4.1, 'Affaires': 3.8, 'Boutique': 4.0},
            'Solo': {'Luxe': 3.8, 'Riad': 4.2, 'Budget': 4.3, 'Affaires': 3.5, 'Boutique': 4.1},
            'Groupe': {'Luxe': 4.0, 'Riad': 4.1, 'Budget': 4.4, 'Affaires': 3.2, 'Boutique': 3.9}
        }
        
        # Chaque utilisateur note 10-30 hôtels
        for user_id in user_ids:
            user_data = users_df[users_df['user_id'] == user_id].iloc[0]
            type_voyage = user_data['type_voyage']
            budget = user_data['budget']
            
            n_ratings_user = random.randint(10, 30)
            hotels_notes = random.sample(hotel_ids, min(n_ratings_user, len(hotel_ids)))  # CORRECTION ICI
            
            for hotel_id in hotels_notes:
                hotel_data = hotels_df[hotels_df['hotel_id'] == hotel_id].iloc[0]
                categorie_hotel = hotel_data['categorie']
                
                # Rating de base selon le type de voyage et catégorie
                rating_base = preferences_par_type[type_voyage][categorie_hotel]
                
                # Ajustement selon le budget
                if budget == 'Économique' and hotel_data['prix'] == '$$$':
                    rating_base -= 1.0
                elif budget == 'Luxe' and hotel_data['prix'] == '$':
                    rating_base -= 0.8
                
                # Ajustement selon les étoiles
                rating_base += (hotel_data['etoiles'] - 3) * 0.2
                
                # Bruit aléatoire
                rating_final = max(1.0, min(5.0, rating_base + random.gauss(0, 0.3)))
                
                ratings.append({
                    'user_id': user_id,
                    'hotel_id': hotel_id,
                    'rating': round(rating_final, 1),
                    'date_sejour': self.fake.date_between(start_date='-2y', end_date='today')
                })
        
        # Si on n'a pas assez de ratings, en ajouter aléatoirement
        while len(ratings) < n_ratings:
            user_id = random.choice(user_ids)
            hotel_id = random.choice(hotel_ids)
            
            # Vérifier que cette combinaison n'existe pas déjà
            if not any(r['user_id'] == user_id and r['hotel_id'] == hotel_id for r in ratings):
                rating = random.randint(1, 5)
                ratings.append({
                    'user_id': user_id,
                    'hotel_id': hotel_id,
                    'rating': rating,
                    'date_sejour': self.fake.date_between(start_date='-2y', end_date='today')
                })
        
        print(f"✅ {len(ratings)} ratings générés")
        return pd.DataFrame(ratings)
    
    def sauvegarder_donnees(self, dossier='data'):
        """Génère et sauvegarde tous les datasets"""
        print(f"💾 Sauvegarde dans le dossier: {dossier}")
        
        if not os.path.exists(dossier):
            print(f"📁 Création du dossier {dossier}")
            os.makedirs(dossier)
        
        hotels_df = self.generer_hotels()
        hotels_df.to_csv(f'{dossier}/hotels.csv', index=False, encoding='utf-8')
        print("✅ Hôtels sauvegardés")
        
        users_df = self.generer_utilisateurs()
        users_df.to_csv(f'{dossier}/users.csv', index=False, encoding='utf-8')
        print("✅ Utilisateurs sauvegardés")
        
        ratings_df = self.generer_ratings(hotels_df, users_df)
        ratings_df.to_csv(f'{dossier}/ratings.csv', index=False, encoding='utf-8')
        print("✅ Ratings sauvegardés")
        
        print(f"🎉 DONNÉES CRÉÉES AVEC SUCCÈS!")
        print(f"   📊 {len(hotels_df)} hôtels")
        print(f"   👥 {len(users_df)} utilisateurs") 
        print(f"   ⭐ {len(ratings_df)} ratings")
        
        return hotels_df, users_df, ratings_df

if __name__ == "__main__":
    print("=" * 50)
    print("🎯 GÉNÉRATEUR DE DONNÉES HÔTELS MARRAKECH")
    print("=" * 50)
    
    try:
        generateur = DataGenerator()
        hotels, users, ratings = generateur.sauvegarder_donnees()
        
        print("\n" + "=" * 50)
        print("📋 APERÇU DES DONNÉES:")
        print("=" * 50)
        
        print("\n🏨 EXEMPLE HÔTELS:")
        print(hotels[['hotel_id', 'nom', 'categorie', 'localisation']].head(2))
        
        print("\n👥 EXEMPLE UTILISATEURS:")
        print(users[['user_id', 'age', 'type_voyage', 'budget']].head(2))
        
        print("\n⭐ EXEMPLE RATINGS:")
        print(ratings[['user_id', 'hotel_id', 'rating']].head(3))
        
        print(f"\n📈 STATISTIQUES:")
        print(f"   📊 Note moyenne: {ratings['rating'].mean():.2f}/5")
        print(f"   📉 Note min: {ratings['rating'].min()}/5")
        print(f"   📈 Note max: {ratings['rating'].max()}/5")
        
        print(f"\n💾 Fichiers créés dans data/:")
        for file in ['hotels.csv', 'users.csv', 'ratings.csv']:
            file_path = f"../data/{file}"
            if os.path.exists(file_path):
                size = os.path.getsize(file_path) / 1024  # Taille en KB
                print(f"   - {file}: {size:.1f} KB")
        
    except Exception as e:
        print(f"\n❌ ERREUR CRITIQUE: {e}")
        import traceback
        traceback.print_exc()
        