"""KNN recommender implementation.

Uses collaborative filtering (user-based) with cosine similarity.
Given a small list of user ratings (hotel_id, rating) the recommender
predicts ratings for unrated hotels using the k nearest users and returns
top-N recommendations enriched with hotel metadata.
"""
from typing import List, Dict
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity


class HotelRecommender:
    def __init__(self, hotels_df: pd.DataFrame, ratings_df: pd.DataFrame, k: int = 5):
        self.hotels_df = hotels_df.copy()
        self.ratings_df = ratings_df.copy()
        self.k = k

        # Build user-item matrix on initialization
        self.user_item = self._build_user_item_matrix()
        # Index lists for mapping
        self.user_ids = list(self.user_item.index)
        self.hotel_ids = list(self.user_item.columns)

    def _build_user_item_matrix(self) -> pd.DataFrame:
        mat = self.ratings_df.pivot_table(index='user_id', columns='hotel_id', values='rating', aggfunc='mean')
        mat = mat.fillna(0)
        return mat

    def _user_vector_from_ratings(self, user_ratings: List[Dict]) -> np.ndarray:
        vec = np.zeros(len(self.hotel_ids))
        id_to_idx = {hid: i for i, hid in enumerate(self.hotel_ids)}
        for r in user_ratings:
            hid = r.get('hotel_id')
            rating = float(r.get('rating', 0))
            if hid in id_to_idx:
                vec[id_to_idx[hid]] = rating
        return vec

    def _compute_similarities(self, user_vec: np.ndarray) -> np.ndarray:
        if self.user_item.shape[0] == 0:
            return np.array([])
        user_vec = user_vec.reshape(1, -1)
        sims = cosine_similarity(user_vec, self.user_item.values)[0]
        return sims

    def recommend(self, user_ratings: List[Dict], n_recommendations: int = 5) -> List[Dict]:
        """Return top-N recommendations for the provided user_ratings.

        If no similar users are found, fall back to most popular hotels.
        """
        user_vec = self._user_vector_from_ratings(user_ratings)
        sims = self._compute_similarities(user_vec)

        # If there are no users in matrix, return popular hotels
        if sims.size == 0:
            return self._popular_hotels(exclude=[r['hotel_id'] for r in user_ratings], n=n_recommendations)

        # Pair (index, similarity), exclude zero similarities
        idx_sims = [(i, float(s)) for i, s in enumerate(sims) if s > 0]
        idx_sims.sort(key=lambda x: x[1], reverse=True)

        if len(idx_sims) == 0:
            return self._popular_hotels(exclude=[r['hotel_id'] for r in user_ratings], n=n_recommendations)

        neighbors = idx_sims[: self.k]

        predictions = []
        for j, hid in enumerate(self.hotel_ids):
            # skip already rated
            if user_vec[j] > 0:
                continue

            num = 0.0
            den = 0.0
            for ni, sim in neighbors:
                neighbor_rating = float(self.user_item.iloc[ni, j])
                if neighbor_rating > 0:
                    num += sim * neighbor_rating
                    den += sim
            if den > 0:
                pred = num / den
                predictions.append((hid, pred))

        # sort predictions
        predictions.sort(key=lambda x: x[1], reverse=True)

        # if not enough predictions, fill with popular hotels
        recs = []
        for hid, pred in predictions[:n_recommendations]:
            meta = self.hotels_df[self.hotels_df['hotel_id'] == hid]
            if meta.empty:
                continue
            row = meta.iloc[0]
            recs.append({
                'hotel_id': hid,
                'nom': row.get('nom', ''),
                'categorie': row.get('categorie', ''),
                'localisation': row.get('localisation', ''),
                'prix': row.get('prix', ''),
                'etoiles': int(row.get('etoiles', 0)) if not pd.isna(row.get('etoiles', np.nan)) else None,
                'commodites': row.get('commodites', ''),
                'predicted_rating': round(float(pred), 2),
                'reason': 'Utilisateurs similaires'
            })

        if len(recs) < n_recommendations:
            needed = n_recommendations - len(recs)
            popular = self._popular_hotels(exclude=[r['hotel_id'] for r in user_ratings] + [r['hotel_id'] for r in recs], n=needed)
            recs.extend(popular)

        return recs

    def _popular_hotels(self, exclude: List[str] = None, n: int = 5) -> List[Dict]:
        if exclude is None:
            exclude = []
        avg = self.ratings_df.groupby('hotel_id')['rating'].mean().sort_values(ascending=False)
        avg = avg[~avg.index.isin(exclude)]
        results = []
        for hid, val in avg.head(n).items():
            meta = self.hotels_df[self.hotels_df['hotel_id'] == hid]
            if meta.empty:
                continue
            row = meta.iloc[0]
            results.append({
                'hotel_id': hid,
                'nom': row.get('nom', ''),
                'categorie': row.get('categorie', ''),
                'localisation': row.get('localisation', ''),
                'prix': row.get('prix', ''),
                'etoiles': int(row.get('etoiles', 0)) if not pd.isna(row.get('etoiles', np.nan)) else None,
                'commodites': row.get('commodites', ''),
                'predicted_rating': round(float(val), 2),
                'reason': 'Hôtel populaire'
            })
        return results