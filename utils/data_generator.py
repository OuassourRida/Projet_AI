"""
Générateur de données pour le système de recommandation d'hôtels à Marrakech
Génère des données réalistes : hôtels, utilisateurs et ratings
"""

import pandas as pd
import numpy as np
import random
import os
from datetime import datetime, timedelta

try:
    from faker import Faker
except ImportError:
    print("❌ Faker non installé. Installer avec: pip install faker")
    exit(1)


class MarrakechHotelDataGenerator:
    """
    Générateur de données réalistes pour les hôtels de Marrakech
    """
    
    def __init__(self, seed=42):
        """
        Initialise le générateur avec une seed pour la reproductibilité
        
        Args:
            seed (int): Seed pour la génération pseudo-aléatoire
        """
        self.fake = Faker(['fr_FR', 'ar_MA'])  # Français et Arabe marocain
        np.random.seed(seed)
        random.seed(seed)
        Faker.seed(seed)
        
        # Configuration des catégories d'hôtels
        self.categories = ['Luxe', 'Riad', 'Budget', 'Affaires', 'Boutique']
        self.localisations = ['Médina', 'Guéliz', 'Hivernage', 'Palmeraie', 'Kasbah']
        
        # Commodités par catégorie
        self.commodites_par_categorie = {
            'Luxe': ['Piscine', 'SPA', 'WiFi', 'Parking', 'Restaurant gastronomique', 
                    'Room Service', 'Fitness', 'Bar', 'Concierge', 'Hammam'],
            'Riad': ['Terrasse panoramique', 'Petit-déjeuner marocain', 'WiFi', 
                    'Patio traditionnel', 'Cuisine locale', 'Fontaine', 'Jardin andalou'],
            'Budget': ['WiFi gratuit', 'Parking', 'Petit-déjeuner continental', 
                      'Climatisation', 'Salle de bain privée', 'Réception 24h'],
            'Affaires': ['WiFi haut débit', 'Parking gratuit', 'Business Center', 
                        'Petit-déjeuner buffet', 'Salle de réunion', 'Service pressing'],
            'Boutique': ['Piscine design', 'WiFi', 'Décoration unique', 'Restaurant', 
                        'Art local', 'Jardin zen', 'Bibliothèque']
        }
        
        # Hôtels célèbres de Marrakech (pour réalisme)
        self.hotels_celebres = [
            ('La Mamounia', 'Luxe', 'Médina'),
            ('Royal Mansour', 'Luxe', 'Médina'), 
            ('Four Seasons', 'Luxe', 'Hivernage'),
            ('Riad Kniza', 'Riad', 'Médina'),
            ('Hotel Ibis Centre', 'Budget', 'Guéliz'),
            ('Sofitel Marrakech', 'Luxe', 'Palmeraie'),
            ('Le Méridien N\'Fis', 'Affaires', 'Hivernage'),
            ('Riad El Fenn', 'Riad', 'Médina'),
            ('Palais Namaskar', 'Luxe', 'Palmeraie'),
            ('Riad Dar Anika', 'Riad', 'Médina'),
            ('Hotel Atlas Asni', 'Budget', 'Guéliz'),
            ('Movenpick Mansour Eddahbi', 'Affaires', 'Hivernage'),
            ('Villa des Orangers', 'Boutique', 'Médina'),
            ('Es Saadi Gardens', 'Luxe', 'Hivernage'),
            ('Riad Farnatchi', 'Riad', 'Médina')
        ]
    
    def generer_hotels(self, n_hotels=80):
        """
        Génère un dataset réaliste d'hôtels à Marrakech
        
        Args:
            n_hotels (int): Nombre d'hôtels à générer
            
        Returns:
            pd.DataFrame: DataFrame contenant les informations des hôtels
        """
        print(f"🏨 Génération de {n_hotels} hôtels à Marrakech...")
        
        hotels = []
        hotel_id = 1
        
        # Ajouter d'abord les hôtels célèbres
        for nom, categorie, localisation in self.hotels_celebres:
            if hotel_id > n_hotels:
                break
                
            hotel_data = self._generer_hotel_data(hotel_id, nom, categorie, localisation)
            hotels.append(hotel_data)
            hotel_id += 1
        
        # Générer les hôtels restants
        while hotel_id <= n_hotels:
            categorie = np.random.choice(self.categories)
            localisation = np.random.choice(self.localisations)
            nom = self._generer_nom_hotel(categorie, localisation)
            
            hotel_data = self._generer_hotel_data(hotel_id, nom, categorie, localisation)
            hotels.append(hotel_data)
            hotel_id += 1
        
        print(f"✅ {len(hotels)} hôtels générés")
        return pd.DataFrame(hotels)
    
    def _generer_hotel_data(self, hotel_id, nom, categorie, localisation):
        """
        Génère les données complètes pour un hôtel
        
        Args:
            hotel_id (int): ID unique de l'hôtel
            nom (str): Nom de l'hôtel
            categorie (str): Catégorie de l'hôtel
            localisation (str): Localisation de l'hôtel
            
        Returns:
            dict: Données complètes de l'hôtel
        """
        # Prix selon la catégorie
        prix_mapping = {
            'Luxe': random.randint(300, 800),
            'Riad': random.randint(120, 350),
            'Budget': random.randint(40, 120),
            'Affaires': random.randint(100, 250),
            'Boutique': random.randint(150, 400)
        }
        
        # Commodités aléatoires selon la catégorie
        commodites_disponibles = self.commodites_par_categorie[categorie]
        n_commodites = random.randint(3, min(6, len(commodites_disponibles)))
        commodites = random.sample(commodites_disponibles, n_commodites)
        
        # Description courte
        description = f"Hôtel {categorie.lower()} situé dans le quartier {localisation} de Marrakech"
        
        return {
            'hotel_id': hotel_id,
            'nom': nom,
            'categorie': categorie,
            'localisation': localisation,
            'prix': prix_mapping[categorie],
            'commodites': ', '.join(commodites),
            'description': description
        }
    
    def _generer_nom_hotel(self, categorie, localisation):
        """
        Génère un nom réaliste pour un hôtel
        
        Args:
            categorie (str): Catégorie de l'hôtel
            localisation (str): Localisation de l'hôtel
            
        Returns:
            str: Nom généré pour l'hôtel
        """
        prefixes = {
            'Luxe': ['Palais', 'Royal', 'Grand Hotel', 'Palace'],
            'Riad': ['Riad', 'Dar', 'Maison'],
            'Budget': ['Hotel', 'Auberge', 'Pension'],
            'Affaires': ['Hotel', 'Business Hotel', 'Executive'],
            'Boutique': ['Villa', 'Maison', 'Residence']
        }
        
        suffixes = {
            'Médina': ['de la Médina', 'Traditionnel', 'des Souks', 'du Centre'],
            'Guéliz': ['Moderne', 'Central', 'City', 'Urbain'],
            'Hivernage': ['Garden', 'Resort', 'des Jardins', 'Paradise'],
            'Palmeraie': ['des Palmiers', 'Oasis', 'Desert', 'Sahara'],
            'Kasbah': ['de la Kasbah', 'Historique', 'Heritage', 'Ancien']
        }
        
        prefix = random.choice(prefixes[categorie])
        suffix = random.choice(suffixes[localisation])
        
        return f"{prefix} {self.fake.last_name()} {suffix}"
    
    def generer_utilisateurs(self, n_utilisateurs=2000):
        """
        Génère des utilisateurs avec des profils réalistes
        
        Args:
            n_utilisateurs (int): Nombre d'utilisateurs à générer
            
        Returns:
            pd.DataFrame: DataFrame contenant les profils utilisateurs
        """
        print(f"👥 Génération de {n_utilisateurs} utilisateurs...")
        
        types_voyage = ['Romantique', 'Affaires', 'Familial', 'Solo', 'Groupe']
        budgets = ['Économique', 'Moyen', 'Luxe']
        nationalites = ['France', 'Allemagne', 'Espagne', 'Italie', 'États-Unis', 
                       'Canada', 'Royaume-Uni', 'Maroc', 'Belgique', 'Pays-Bas']
        
        utilisateurs = []
        
        for i in range(1, n_utilisateurs + 1):
            age = int(np.random.normal(40, 15))  # Distribution normale autour de 40 ans
            age = max(18, min(75, age))  # Limiter entre 18 et 75 ans
            
            # Le type de voyage et budget dépendent de l'âge
            type_voyage, budget = self._determiner_profil_voyage(age)
            nationalite = random.choice(nationalites)
            
            utilisateurs.append({
                'user_id': i,
                'age': age,
                'type_voyage': type_voyage,
                'budget': budget,
                'nationalite': nationalite
            })
        
        print(f"✅ {len(utilisateurs)} utilisateurs générés")
        return pd.DataFrame(utilisateurs)
    
    def _determiner_profil_voyage(self, age):
        """
        Détermine le type de voyage et budget selon l'âge
        
        Args:
            age (int): Âge de l'utilisateur
            
        Returns:
            tuple: (type_voyage, budget)
        """
        if age < 25:
            type_voyage = random.choices(
                ['Solo', 'Groupe', 'Romantique'], 
                weights=[0.4, 0.4, 0.2]
            )[0]
            budget = random.choices(
                ['Économique', 'Moyen', 'Luxe'],
                weights=[0.6, 0.3, 0.1]
            )[0]
        elif age < 40:
            type_voyage = random.choices(
                ['Romantique', 'Affaires', 'Familial', 'Solo'],
                weights=[0.3, 0.3, 0.2, 0.2]
            )[0]
            budget = random.choices(
                ['Économique', 'Moyen', 'Luxe'],
                weights=[0.2, 0.5, 0.3]
            )[0]
        elif age < 60:
            type_voyage = random.choices(
                ['Familial', 'Affaires', 'Romantique'],
                weights=[0.4, 0.4, 0.2]
            )[0]
            budget = random.choices(
                ['Économique', 'Moyen', 'Luxe'],
                weights=[0.1, 0.4, 0.5]
            )[0]
        else:  # 60+
            type_voyage = random.choices(
                ['Romantique', 'Familial', 'Groupe'],
                weights=[0.4, 0.3, 0.3]
            )[0]
            budget = random.choices(
                ['Moyen', 'Luxe'],
                weights=[0.4, 0.6]
            )[0]
        
        return type_voyage, budget
    
    def generer_ratings(self, hotels_df, users_df, n_ratings=50000):
        """
        Génère des ratings réalistes basés sur les profils utilisateurs
        
        Args:
            hotels_df (pd.DataFrame): DataFrame des hôtels
            users_df (pd.DataFrame): DataFrame des utilisateurs
            n_ratings (int): Nombre de ratings cibles
            
        Returns:
            pd.DataFrame: DataFrame contenant les ratings
        """
        print(f"⭐ Génération de {n_ratings} ratings...")
        
        ratings = []
        
        # Matrice des préférences par type de voyage et catégorie d'hôtel
        preferences = {
            'Romantique': {'Luxe': 4.6, 'Riad': 4.8, 'Budget': 2.2, 'Affaires': 2.8, 'Boutique': 4.4},
            'Affaires': {'Luxe': 4.3, 'Riad': 3.2, 'Budget': 3.6, 'Affaires': 4.7, 'Boutique': 3.8},
            'Familial': {'Luxe': 4.4, 'Riad': 4.0, 'Budget': 4.2, 'Affaires': 3.5, 'Boutique': 4.1},
            'Solo': {'Luxe': 3.9, 'Riad': 4.5, 'Budget': 4.4, 'Affaires': 3.3, 'Boutique': 4.2},
            'Groupe': {'Luxe': 4.1, 'Riad': 4.2, 'Budget': 4.5, 'Affaires': 3.1, 'Boutique': 3.9}
        }
        
        # Ajustement selon le budget
        budget_adjustment = {
            'Économique': {'Luxe': -1.5, 'Riad': -0.3, 'Budget': 0.5, 'Affaires': 0.0, 'Boutique': -0.8},
            'Moyen': {'Luxe': -0.3, 'Riad': 0.2, 'Budget': 0.2, 'Affaires': 0.3, 'Boutique': 0.2},
            'Luxe': {'Luxe': 0.4, 'Riad': 0.3, 'Budget': -1.0, 'Affaires': 0.1, 'Boutique': 0.3}
        }
        
        # Générer les ratings
        ratings_per_user = n_ratings // len(users_df)
        
        for _, user in users_df.iterrows():
            user_id = user['user_id']
            type_voyage = user['type_voyage']
            budget = user['budget']
            age = user['age']
            
            # Nombre de ratings pour cet utilisateur (variation autour de la moyenne)
            n_user_ratings = max(5, int(np.random.poisson(ratings_per_user)))
            n_user_ratings = min(n_user_ratings, len(hotels_df))
            
            # Sélectionner aléatoirement les hôtels à noter
            hotels_sample = hotels_df.sample(n_user_ratings)
            
            for _, hotel in hotels_sample.iterrows():
                hotel_id = hotel['hotel_id']
                categorie = hotel['categorie']
                prix = hotel['prix']
                
                # Rating de base selon les préférences
                base_rating = preferences[type_voyage][categorie]
                
                # Ajustement selon le budget
                base_rating += budget_adjustment[budget][categorie]
                
                # Ajustement selon le prix (cohérence budget-prix)
                if budget == 'Économique' and prix > 200:
                    base_rating -= 0.8
                elif budget == 'Luxe' and prix < 100:
                    base_rating -= 0.5
                
                # Ajustement selon l'âge (les plus âgés sont plus exigeants)
                if age > 50:
                    base_rating -= 0.2
                elif age < 30:
                    base_rating += 0.1
                
                # Ajouter du bruit aléatoire
                noise = np.random.normal(0, 0.4)
                final_rating = base_rating + noise
                
                # Limiter entre 1 et 5
                final_rating = max(1.0, min(5.0, final_rating))
                final_rating = round(final_rating * 2) / 2  # Arrondir aux 0.5
                
                # Date de séjour aléatoire dans les 2 dernières années
                date_sejour = self.fake.date_between(start_date='-2y', end_date='today')
                
                ratings.append({
                    'user_id': user_id,
                    'hotel_id': hotel_id,
                    'rating': final_rating,
                    'date_sejour': date_sejour
                })
        
        # Limiter au nombre de ratings demandés
        if len(ratings) > n_ratings:
            ratings = random.sample(ratings, n_ratings)
        
        print(f"✅ {len(ratings)} ratings générés")
        return pd.DataFrame(ratings)
    
    def sauvegarder_donnees(self, dossier='data'):
        """
        Génère et sauvegarde tous les datasets
        
        Args:
            dossier (str): Dossier de destination
            
        Returns:
            tuple: (hotels_df, users_df, ratings_df)
        """
        print(f"💾 Sauvegarde des données dans '{dossier}'...")
        
        # Créer le dossier si nécessaire
        os.makedirs(dossier, exist_ok=True)
        
        # Générer les datasets
        hotels_df = self.generer_hotels(80)
        users_df = self.generer_utilisateurs(2000)
        ratings_df = self.generer_ratings(hotels_df, users_df, 50000)
        
        # Sauvegarder en CSV
        hotels_df.to_csv(f'{dossier}/hotels.csv', index=False, encoding='utf-8')
        users_df.to_csv(f'{dossier}/users.csv', index=False, encoding='utf-8')
        ratings_df.to_csv(f'{dossier}/ratings.csv', index=False, encoding='utf-8')
        
        # Afficher les statistiques
        self._afficher_statistiques(hotels_df, users_df, ratings_df)
        
        print(f"🎉 Données sauvegardées avec succès dans '{dossier}/'!")
        return hotels_df, users_df, ratings_df
    
    def _afficher_statistiques(self, hotels_df, users_df, ratings_df):
        """
        Affiche les statistiques des données générées
        """
        print("\n📊 STATISTIQUES DES DONNÉES GÉNÉRÉES")
        print("=" * 50)
        
        print(f"🏨 HÔTELS: {len(hotels_df)}")
        print(f"   Catégories: {hotels_df['categorie'].value_counts().to_dict()}")
        print(f"   Localisations: {hotels_df['localisation'].value_counts().to_dict()}")
        print(f"   Prix moyen: {hotels_df['prix'].mean():.0f}€")
        
        print(f"\n👥 UTILISATEURS: {len(users_df)}")
        print(f"   Âge moyen: {users_df['age'].mean():.1f} ans")
        print(f"   Types de voyage: {users_df['type_voyage'].value_counts().to_dict()}")
        print(f"   Budgets: {users_df['budget'].value_counts().to_dict()}")
        
        print(f"\n⭐ RATINGS: {len(ratings_df)}")
        print(f"   Note moyenne: {ratings_df['rating'].mean():.2f}/5")
        print(f"   Distribution: {ratings_df['rating'].value_counts().sort_index().to_dict()}")
        print(f"   Ratings par utilisateur: {len(ratings_df) / len(users_df):.1f}")


if __name__ == "__main__":
    print("🎯 GÉNÉRATEUR DE DONNÉES - SYSTÈME DE RECOMMANDATION MARRAKECH")
    print("=" * 70)
    
    try:
        # Créer et exécuter le générateur
        generateur = MarrakechHotelDataGenerator()
        hotels_df, users_df, ratings_df = generateur.sauvegarder_donnees()
        
        # Aperçu des données
        print("\n📋 APERÇU DES DONNÉES:")
        print("=" * 30)
        
        print("\n🏨 Exemple d'hôtels:")
        print(hotels_df[['hotel_id', 'nom', 'categorie', 'localisation', 'prix']].head(3))
        
        print("\n👥 Exemple d'utilisateurs:")
        print(users_df[['user_id', 'age', 'type_voyage', 'budget', 'nationalite']].head(3))
        
        print("\n⭐ Exemple de ratings:")
        print(ratings_df[['user_id', 'hotel_id', 'rating', 'date_sejour']].head(5))
        
    except Exception as e:
        print(f"\n❌ ERREUR: {e}")
        import traceback
        traceback.print_exc()
        