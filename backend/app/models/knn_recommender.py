"""
Système de recommandation d'hôtels utilisant KNN et filtrage collaboratif
Utilise la similarité cosinus pour trouver des utilisateurs similaires
"""

import pandas as pd
import numpy as np
from sklearn.neighbors import NearestNeighbors
from sklearn.metrics.pairwise import cosine_similarity
import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class HotelRecommender:
    """
    Classe principale pour le système de recommandation d'hôtels
    Utilise KNN avec similarité cosinus pour le filtrage collaboratif
    """
    
    def __init__(self, k=5):
        """
        Initialise le système de recommandation
        
        Args:
            k (int): Nombre de voisins pour KNN
        """
        self.k = k
        self.hotels_df = None
        self.users_df = None
        self.ratings_df = None
        self.user_item_matrix = None
        self.model = None
        self._data_loaded = False
        
    def load_data(self):
        """
        Charge les données depuis les fichiers CSV
        
        Raises:
            FileNotFoundError: Si les fichiers de données n'existent pas
        """
        try:
            base_path = os.path.join(os.path.dirname(__file__), '../../../data')
            
            self.hotels_df = pd.read_csv(os.path.join(base_path, 'hotels.csv'))
            self.users_df = pd.read_csv(os.path.join(base_path, 'users.csv'))
            self.ratings_df = pd.read_csv(os.path.join(base_path, 'ratings.csv'))
            
            logger.info(f"Données chargées: {len(self.hotels_df)} hôtels, "
                       f"{len(self.users_df)} utilisateurs, {len(self.ratings_df)} ratings")
            
            # Calculer les moyennes des ratings par hôtel
            hotel_avg_ratings = self.ratings_df.groupby('hotel_id')['rating'].mean()
            self.hotels_df['avg_rating'] = self.hotels_df['hotel_id'].map(hotel_avg_ratings).fillna(0)
            
            self._data_loaded = True
            self._prepare_user_item_matrix()
            
        except FileNotFoundError as e:
            logger.error(f"Erreur lors du chargement des données: {e}")
            raise
            
    def _prepare_user_item_matrix(self):
        """
        Prépare la matrice utilisateur-item pour l'algorithme KNN
        """
        if not self._data_loaded:
            self.load_data()
            
        # Créer la matrice pivot utilisateur-item
        self.user_item_matrix = self.ratings_df.pivot_table(
            index='user_id',
            columns='hotel_id', 
            values='rating',
            fill_value=0
        )
        
        logger.info(f"Matrice utilisateur-item créée: {self.user_item_matrix.shape}")
        
    def _train_model(self):
        """
        Entraîne le modèle KNN avec similarité cosinus
        """
        if self.user_item_matrix is None:
            self._prepare_user_item_matrix()
            
        # Initialiser le modèle KNN avec similarité cosinus
        self.model = NearestNeighbors(
            n_neighbors=min(self.k, len(self.user_item_matrix) - 1),
            metric='cosine',
            algorithm='brute'
        )
        
        # Entraîner sur la matrice utilisateur-item
        self.model.fit(self.user_item_matrix.values)
        
        logger.info(f"Modèle KNN entraîné avec k={self.k}")
        
    def find_similar_users(self, user_ratings):
        """
        Trouve les k utilisateurs les plus similaires
        
        Args:
            user_ratings (dict): Ratings de l'utilisateur {hotel_id: rating}
            
        Returns:
            list: Liste des utilisateurs similaires avec leurs scores de similarité
        """
        if self.model is None:
            self._train_model()
            
        # Créer le vecteur utilisateur
        user_vector = np.zeros(len(self.user_item_matrix.columns))
        
        for hotel_id, rating in user_ratings.items():
            if hotel_id in self.user_item_matrix.columns:
                hotel_idx = self.user_item_matrix.columns.get_loc(hotel_id)
                user_vector[hotel_idx] = rating
                
        # Trouver les voisins les plus proches
        distances, indices = self.model.kneighbors([user_vector])
        
        similar_users = []
        for distance, idx in zip(distances[0], indices[0]):
            # Convertir la distance cosinus en similarité
            similarity = 1 - distance
            user_id = self.user_item_matrix.index[idx]
            
            similar_users.append({
                'user_id': user_id,
                'similarity': similarity
            })
            
        return similar_users
        
    def predict_ratings(self, user_ratings, hotel_ids=None):
        """
        Prédit les ratings pour les hôtels non notés
        
        Args:
            user_ratings (dict): Ratings existants de l'utilisateur
            hotel_ids (list): Liste des hotel_id à prédire (optionnel)
            
        Returns:
            dict: Prédictions {hotel_id: predicted_rating}
        """
        similar_users = self.find_similar_users(user_ratings)
        
        # Hotels à prédire (tous sauf ceux déjà notés si non spécifié)
        if hotel_ids is None:
            all_hotels = set(self.user_item_matrix.columns)
            rated_hotels = set(user_ratings.keys())
            hotel_ids = list(all_hotels - rated_hotels)
            
        predictions = {}
        
        for hotel_id in hotel_ids:
            if hotel_id not in self.user_item_matrix.columns:
                continue
                
            weighted_sum = 0
            similarity_sum = 0
            
            # Calculer la moyenne pondérée des ratings des utilisateurs similaires
            for similar_user in similar_users:
                user_id = similar_user['user_id']
                similarity = similar_user['similarity']
                
                # Rating de cet utilisateur pour cet hôtel
                rating = self.user_item_matrix.loc[user_id, hotel_id]
                
                if rating > 0:  # L'utilisateur a noté cet hôtel
                    weighted_sum += rating * similarity
                    similarity_sum += similarity
                    
            # Prédire le rating si on a des données
            if similarity_sum > 0:
                predicted_rating = weighted_sum / similarity_sum
                predictions[hotel_id] = round(predicted_rating, 2)
                
        return predictions
        
    def get_recommendations(self, user_ratings, n_recommendations=5):
        """
        Génère les recommandations personnalisées
        
        Args:
            user_ratings (dict): Ratings de l'utilisateur {hotel_id: rating}
            n_recommendations (int): Nombre de recommandations à retourner
            
        Returns:
            list: Liste des recommandations avec détails
        """
        try:
            # Gestion du cold start - si très peu de ratings
            if len(user_ratings) < 2:
                return self._get_popular_recommendations(n_recommendations)
                
            # Prédire les ratings pour tous les hôtels non notés
            predictions = self.predict_ratings(user_ratings)
            
            # Si pas assez de prédictions, compléter avec les populaires
            if len(predictions) < n_recommendations:
                popular = self._get_popular_recommendations(n_recommendations - len(predictions))
                return self._format_recommendations(predictions, user_ratings) + popular
                
            # Trier par rating prédit décroissant
            sorted_predictions = sorted(
                predictions.items(), 
                key=lambda x: x[1], 
                reverse=True
            )
            
            # Prendre les top n_recommendations
            top_predictions = dict(sorted_predictions[:n_recommendations])
            
            return self._format_recommendations(top_predictions, user_ratings)
            
        except Exception as e:
            logger.error(f"Erreur lors de la génération des recommandations: {e}")
            return self._get_popular_recommendations(n_recommendations)
            
    def _format_recommendations(self, predictions, user_ratings):
        """
        Formate les recommandations avec les détails des hôtels
        
        Args:
            predictions (dict): Prédictions {hotel_id: predicted_rating}
            user_ratings (dict): Ratings existants de l'utilisateur
            
        Returns:
            list: Recommandations formatées
        """
        recommendations = []
        
        for hotel_id, predicted_rating in predictions.items():
            # Récupérer les détails de l'hôtel
            hotel = self.hotels_df[self.hotels_df['hotel_id'] == hotel_id]
            
            if not hotel.empty:
                hotel = hotel.iloc[0]
                
                # Générer une explication personnalisée
                explanation = self._generate_explanation(user_ratings, hotel)
                
                recommendations.append({
                    'hotel_id': hotel_id,
                    'nom': hotel['nom'],
                    'predicted_rating': predicted_rating,
                    'categorie': hotel['categorie'],
                    'localisation': hotel['localisation'],
                    'prix': hotel['prix'],
                    'commodites': hotel['commodites'],
                    'description': hotel.get('description', ''),
                    'explanation': explanation
                })
                
        return recommendations
        
    def _generate_explanation(self, user_ratings, hotel):
        """
        Génère une explication personnalisée pour la recommandation
        
        Args:
            user_ratings (dict): Ratings de l'utilisateur
            hotel (pd.Series): Informations de l'hôtel
            
        Returns:
            str: Explication de la recommandation
        """
        # Analyser les préférences de l'utilisateur
        user_hotel_ids = list(user_ratings.keys())
        user_hotels = self.hotels_df[self.hotels_df['hotel_id'].isin(user_hotel_ids)]
        
        if user_hotels.empty:
            return "Hôtel populaire auprès des utilisateurs avec des goûts similaires"
            
        # Préférences déduites
        high_rated = [hid for hid, rating in user_ratings.items() if rating >= 4]
        
        if high_rated:
            high_rated_hotels = self.hotels_df[
                self.hotels_df['hotel_id'].isin(high_rated)
            ]
            
            # Vérifier les similarités
            if not high_rated_hotels.empty:
                # Catégorie similaire
                if hotel['categorie'] in high_rated_hotels['categorie'].values:
                    return f"Similaire aux hôtels {hotel['categorie'].lower()} que vous avez bien notés"
                    
                # Localisation similaire  
                if hotel['localisation'] in high_rated_hotels['localisation'].values:
                    return f"Dans {hotel['localisation']}, comme vos hôtels préférés"
                    
                # Prix similaire
                price_range = high_rated_hotels['prix'].mean()
                if abs(hotel['prix'] - price_range) < 100:
                    return "Dans votre gamme de prix préférée"
                    
        return "Recommandé par des utilisateurs aux goûts similaires aux vôtres"
        
    def _get_popular_recommendations(self, n_recommendations=5):
        """
        Retourne les hôtels les plus populaires (stratégie cold start)
        
        Args:
            n_recommendations (int): Nombre de recommandations
            
        Returns:
            list: Recommandations populaires
        """
        # Calculer la popularité basée sur le nombre de ratings et la moyenne
        hotel_stats = self.ratings_df.groupby('hotel_id').agg({
            'rating': ['count', 'mean']
        }).round(2)
        
        hotel_stats.columns = ['count', 'avg_rating']
        
        # Score de popularité = moyenne pondérée par le nombre de ratings
        hotel_stats['popularity_score'] = (
            hotel_stats['avg_rating'] * np.log(hotel_stats['count'] + 1)
        )
        
        # Top hôtels populaires
        top_popular = hotel_stats.nlargest(n_recommendations, 'popularity_score')
        
        recommendations = []
        for hotel_id in top_popular.index:
            hotel = self.hotels_df[self.hotels_df['hotel_id'] == hotel_id].iloc[0]
            avg_rating = top_popular.loc[hotel_id, 'avg_rating']
            
            recommendations.append({
                'hotel_id': hotel_id,
                'nom': hotel['nom'],
                'predicted_rating': avg_rating,
                'categorie': hotel['categorie'],
                'localisation': hotel['localisation'],
                'prix': hotel['prix'],
                'commodites': hotel['commodites'],
                'description': hotel.get('description', ''),
                'explanation': f"Hôtel populaire avec {avg_rating}/5 étoiles en moyenne"
            })
            
        return recommendations
        
    def get_all_hotels(self):
        """
        Retourne tous les hôtels disponibles
        
        Returns:
            list: Liste de tous les hôtels
        """
        if not self._data_loaded:
            self.load_data()
            
        hotels = []
        for _, hotel in self.hotels_df.iterrows():
            hotels.append({
                'hotel_id': hotel['hotel_id'],
                'nom': hotel['nom'],
                'categorie': hotel['categorie'],
                'localisation': hotel['localisation'],
                'prix': hotel['prix'],
                'commodites': hotel['commodites'],
                'description': hotel.get('description', ''),
                'avg_rating': self._get_hotel_avg_rating(hotel['hotel_id'])
            })
            
        return hotels
        
    def _get_hotel_avg_rating(self, hotel_id):
        """
        Calcule la note moyenne d'un hôtel
        
        Args:
            hotel_id: ID de l'hôtel
            
        Returns:
            float: Note moyenne
        """
        hotel_ratings = self.ratings_df[self.ratings_df['hotel_id'] == hotel_id]
        if hotel_ratings.empty:
            return 0.0
        return round(hotel_ratings['rating'].mean(), 1)
