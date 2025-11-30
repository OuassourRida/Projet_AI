import React, { useState, useEffect } from 'react';
import { getHotels, getRecommendations } from './services/api';
import HotelCard from './components/HotelCard';
import Recommendations from './components/Recommendations';
import './App.css';

function App() {
  const [hotels, setHotels] = useState([]);
  const [userRatings, setUserRatings] = useState({});
  const [recommendations, setRecommendations] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [step, setStep] = useState('rating'); // 'rating' or 'recommendations'

  useEffect(() => {
    loadHotels();
  }, []);

  const loadHotels = async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await getHotels();
      setHotels(data);
    } catch (err) {
      setError('Impossible de charger les hôtels. Assurez-vous que le serveur est lancé.');
      console.error('Error loading hotels:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleRatingChange = (hotelId, rating) => {
    setUserRatings(prev => ({
      ...prev,
      [hotelId]: rating
    }));
  };

  const handleGetRecommendations = async () => {
    setLoading(true);
    setError(null);
    try {
      // Formater les ratings pour l'API
      const ratings = Object.entries(userRatings).map(([hotel_id, rating]) => ({
        hotel_id,
        rating
      }));

      if (ratings.length === 0) {
        setError('Veuillez noter au moins un hôtel.');
        setLoading(false);
        return;
      }

      const data = await getRecommendations(ratings);
      setRecommendations(data);
      setStep('recommendations');
    } catch (err) {
      setError('Erreur lors de la génération des recommandations. Vérifiez le serveur.');
      console.error('Error getting recommendations:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleResetRatings = () => {
    setUserRatings({});
    setRecommendations([]);
    setStep('rating');
    setError(null);
  };

  return (
    <div className="App">
      <header className="app-header">
        <h1>🏨 Système de Recommandation d'Hôtels Marrakech</h1>
        <p>Notez quelques hôtels pour recevoir des recommandations personnalisées</p>
      </header>

      {error && (
        <div className="error-banner">
          <p>⚠️ {error}</p>
        </div>
      )}

      {loading && (
        <div className="loading">
          <p>Chargement...</p>
        </div>
      )}

      {!loading && step === 'rating' && (
        <div className="rating-section">
          <div className="section-header">
            <h2>Étape 1: Évaluez les hôtels</h2>
            <p>({Object.keys(userRatings).length} hôtels notés)</p>
          </div>

          <div className="hotels-grid">
            {hotels.length === 0 ? (
              <p className="no-data">Aucun hôtel disponible</p>
            ) : (
              hotels.map(hotel => (
                <HotelCard
                  key={hotel.hotel_id}
                  hotel={hotel}
                  rating={userRatings[hotel.hotel_id] || 0}
                  onRatingChange={handleRatingChange}
                />
              ))
            )}
          </div>

          <div className="action-buttons">
            <button
              className="btn btn-primary"
              onClick={handleGetRecommendations}
              disabled={Object.keys(userRatings).length === 0}
            >
              Obtenir les recommandations →
            </button>
          </div>
        </div>
      )}

      {!loading && step === 'recommendations' && (
        <div className="recommendations-section">
          <Recommendations
            recommendations={recommendations}
            onReset={handleResetRatings}
          />
        </div>
      )}
    </div>
  );
}

export default App;
