"""
Module pour calculer la similarité entre utilisateurs
Utilise différentes métriques de similarité pour le filtrage collaboratif
"""

import numpy as np
from scipy.spatial.distance import cosine
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd


def cosine_similarity_users(user1_ratings, user2_ratings):
    """
    Calcule la similarité cosinus entre deux utilisateurs
    
    Args:
        user1_ratings (dict): Ratings du premier utilisateur {hotel_id: rating}
        user2_ratings (dict): Ratings du second utilisateur {hotel_id: rating}
        
    Returns:
        float: Similarité cosinus entre 0 et 1
    """
    # Trouver les hôtels communs
    common_hotels = set(user1_ratings.keys()) & set(user2_ratings.keys())
    
    if len(common_hotels) == 0:
        return 0.0
        
    # Créer les vecteurs pour les hôtels communs
    ratings1 = [user1_ratings[hotel] for hotel in common_hotels]
    ratings2 = [user2_ratings[hotel] for hotel in common_hotels]
    
    # Calculer la similarité cosinus
    try:
        similarity = cosine_similarity([ratings1], [ratings2])[0][0]
        return max(0.0, similarity)  # Assurer que c'est positif
    except:
        return 0.0


def pearson_correlation(user1_ratings, user2_ratings):
    """
    Calcule la corrélation de Pearson entre deux utilisateurs
    
    Args:
        user1_ratings (dict): Ratings du premier utilisateur
        user2_ratings (dict): Ratings du second utilisateur
        
    Returns:
        float: Corrélation de Pearson entre -1 et 1
    """
    # Trouver les hôtels communs
    common_hotels = set(user1_ratings.keys()) & set(user2_ratings.keys())
    
    if len(common_hotels) < 2:
        return 0.0
        
    # Créer les vecteurs pour les hôtels communs
    ratings1 = [user1_ratings[hotel] for hotel in common_hotels]
    ratings2 = [user2_ratings[hotel] for hotel in common_hotels]
    
    # Calculer la corrélation de Pearson
    correlation = np.corrcoef(ratings1, ratings2)[0, 1]
    
    # Remplacer NaN par 0
    if np.isnan(correlation):
        return 0.0
        
    return correlation


def euclidean_similarity(user1_ratings, user2_ratings):
    """
    Calcule la similarité euclidienne entre deux utilisateurs
    
    Args:
        user1_ratings (dict): Ratings du premier utilisateur
        user2_ratings (dict): Ratings du second utilisateur
        
    Returns:
        float: Similarité euclidienne normalisée entre 0 et 1
    """
    # Trouver les hôtels communs
    common_hotels = set(user1_ratings.keys()) & set(user2_ratings.keys())
    
    if len(common_hotels) == 0:
        return 0.0
        
    # Calculer la distance euclidienne
    sum_squares = sum([
        (user1_ratings[hotel] - user2_ratings[hotel]) ** 2 
        for hotel in common_hotels
    ])
    
    # Normaliser la similarité (plus la distance est petite, plus la similarité est grande)
    # Utiliser 1 / (1 + distance) pour obtenir une valeur entre 0 et 1
    similarity = 1 / (1 + np.sqrt(sum_squares))
    
    return similarity


def jaccard_similarity(user1_ratings, user2_ratings, threshold=3.5):
    """
    Calcule la similarité de Jaccard basée sur les hôtels aimés
    (ratings >= threshold)
    
    Args:
        user1_ratings (dict): Ratings du premier utilisateur
        user2_ratings (dict): Ratings du second utilisateur
        threshold (float): Seuil pour considérer qu'un hôtel est aimé
        
    Returns:
        float: Similarité de Jaccard entre 0 et 1
    """
    # Hôtels aimés par chaque utilisateur
    liked_by_user1 = set([hotel for hotel, rating in user1_ratings.items() if rating >= threshold])
    liked_by_user2 = set([hotel for hotel, rating in user2_ratings.items() if rating >= threshold])
    
    # Intersection et union
    intersection = len(liked_by_user1 & liked_by_user2)
    union = len(liked_by_user1 | liked_by_user2)
    
    if union == 0:
        return 0.0
        
    return intersection / union


def adjusted_cosine_similarity(ratings_matrix, user1_id, user2_id):
    """
    Calcule la similarité cosinus ajustée entre deux utilisateurs
    Soustrait la moyenne de chaque utilisateur pour normaliser
    
    Args:
        ratings_matrix (pd.DataFrame): Matrice utilisateur-item
        user1_id: ID du premier utilisateur
        user2_id: ID du second utilisateur
        
    Returns:
        float: Similarité cosinus ajustée
    """
    if user1_id not in ratings_matrix.index or user2_id not in ratings_matrix.index:
        return 0.0
        
    # Ratings des deux utilisateurs
    user1_ratings = ratings_matrix.loc[user1_id]
    user2_ratings = ratings_matrix.loc[user2_id]
    
    # Hôtels notés par les deux utilisateurs
    common_mask = (user1_ratings > 0) & (user2_ratings > 0)
    
    if common_mask.sum() == 0:
        return 0.0
        
    # Moyennes des utilisateurs (seulement pour les hôtels notés)
    user1_mean = user1_ratings[user1_ratings > 0].mean()
    user2_mean = user2_ratings[user2_ratings > 0].mean()
    
    # Ratings ajustés pour les hôtels communs
    user1_adjusted = user1_ratings[common_mask] - user1_mean
    user2_adjusted = user2_ratings[common_mask] - user2_mean
    
    # Calcul de la similarité cosinus
    try:
        similarity = cosine_similarity([user1_adjusted], [user2_adjusted])[0][0]
        return max(0.0, similarity)
    except:
        return 0.0


class SimilarityCalculator:
    """
    Classe utilitaire pour calculer différents types de similarités
    """
    
    def __init__(self, method='cosine'):
        """
        Initialise le calculateur de similarité
        
        Args:
            method (str): Méthode de similarité ('cosine', 'pearson', 'euclidean', 'jaccard')
        """
        self.method = method
        self.similarity_functions = {
            'cosine': cosine_similarity_users,
            'pearson': pearson_correlation, 
            'euclidean': euclidean_similarity,
            'jaccard': jaccard_similarity
        }
        
    def calculate_similarity(self, user1_ratings, user2_ratings):
        """
        Calcule la similarité selon la méthode choisie
        
        Args:
            user1_ratings (dict): Ratings du premier utilisateur
            user2_ratings (dict): Ratings du second utilisateur
            
        Returns:
            float: Score de similarité
        """
        if self.method not in self.similarity_functions:
            raise ValueError(f"Méthode {self.method} non supportée")
            
        return self.similarity_functions[self.method](user1_ratings, user2_ratings)
        
    def find_most_similar_users(self, target_ratings, all_users_ratings, k=5):
        """
        Trouve les k utilisateurs les plus similaires
        
        Args:
            target_ratings (dict): Ratings de l'utilisateur cible
            all_users_ratings (dict): Ratings de tous les utilisateurs {user_id: {hotel_id: rating}}
            k (int): Nombre d'utilisateurs similaires à retourner
            
        Returns:
            list: Liste des utilisateurs similaires triés par similarité décroissante
        """
        similarities = []
        
        for user_id, user_ratings in all_users_ratings.items():
            similarity = self.calculate_similarity(target_ratings, user_ratings)
            similarities.append({
                'user_id': user_id,
                'similarity': similarity
            })
            
        # Trier par similarité décroissante
        similarities.sort(key=lambda x: x['similarity'], reverse=True)
        
        return similarities[:k]
