"""Unit tests for the recommendation backend."""
import pytest
import sys
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent / 'app'))

from app.models.knn_recommender import recommend, _match_input_to_ids, load_tables
from app.models.similarity import cosine_similarity, pearson_similarity, euclidean_distance
import numpy as np


class TestRecommender:
    """Test recommendation engine."""
    
    def test_load_tables(self):
        """Test that data loads successfully."""
        hotels, ratings = load_tables()
        assert hotels is not None
        assert ratings is not None
        assert len(hotels) > 0
        assert len(ratings) > 0
        assert 'hotel_id' in hotels.columns
        assert 'nom' in hotels.columns
        assert 'rating' in ratings.columns
    
    def test_recommend_returns_list(self):
        """Test that recommend returns a list."""
        result = recommend(['La Mamounia'], top_k=5)
        assert isinstance(result, list)
        assert len(result) <= 5
    
    def test_recommend_returns_dicts(self):
        """Test that recommendations are well-formed."""
        result = recommend(['La Mamounia'], top_k=3)
        for rec in result:
            assert isinstance(rec, dict)
            assert 'id' in rec
            assert 'name' in rec
            assert 'category' in rec
            assert 'avg_rating' in rec
    
    def test_recommend_excludes_input(self):
        """Test that input hotels are excluded from recommendations."""
        result = recommend(['H001'], top_k=10)
        hotel_ids = [rec['id'] for rec in result]
        assert 'H001' not in hotel_ids
    
    def test_recommend_by_name(self):
        """Test matching hotels by name."""
        result = recommend(['La Mamounia'], top_k=10)
        # Should exclude La Mamounia from results
        names = [rec['name'] for rec in result]
        assert 'La Mamounia' not in names
        assert len(result) > 0
    
    def test_recommend_top_k(self):
        """Test that top_k is respected."""
        result = recommend([], top_k=3)
        assert len(result) <= 3
    
    def test_recommend_empty_input(self):
        """Test with no input hotels."""
        result = recommend([], top_k=5)
        assert isinstance(result, list)
        assert len(result) > 0
    
    def test_recommend_returns_rated_hotels(self):
        """Test that recommendations have ratings."""
        result = recommend([], top_k=5)
        for rec in result:
            assert rec['avg_rating'] >= 0
            assert rec['avg_rating'] <= 5


class TestSimilarity:
    """Test similarity computation functions."""
    
    def test_cosine_similarity_identical(self):
        """Test cosine similarity of identical vectors."""
        vec = np.array([1, 0, 1])
        similarity = cosine_similarity(vec, vec)
        assert similarity == pytest.approx(1.0, abs=0.01)
    
    def test_cosine_similarity_orthogonal(self):
        """Test cosine similarity of orthogonal vectors."""
        vec1 = np.array([1, 0, 0])
        vec2 = np.array([0, 1, 0])
        similarity = cosine_similarity(vec1, vec2)
        assert similarity == pytest.approx(0.0, abs=0.01)
    
    def test_cosine_similarity_opposite(self):
        """Test cosine similarity of opposite vectors."""
        vec1 = np.array([1, 1, 1])
        vec2 = np.array([-1, -1, -1])
        similarity = cosine_similarity(vec1, vec2)
        assert similarity == pytest.approx(-1.0, abs=0.01)
    
    def test_pearson_similarity_identical(self):
        """Test Pearson similarity of identical vectors."""
        vec = np.array([1.0, 2.0, 3.0, 4.0])
        similarity = pearson_similarity(vec, vec)
        assert similarity == pytest.approx(1.0, abs=0.01)
    
    def test_euclidean_distance_identical(self):
        """Test Euclidean distance of identical vectors."""
        vec = np.array([1.0, 2.0, 3.0])
        distance = euclidean_distance(vec, vec)
        assert distance == pytest.approx(1.0, abs=0.01)
    
    def test_euclidean_distance_empty(self):
        """Test Euclidean distance with empty vectors."""
        vec1 = np.array([])
        vec2 = np.array([])
        distance = euclidean_distance(vec1, vec2)
        assert distance == 0.0


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
