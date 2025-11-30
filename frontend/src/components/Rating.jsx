import React, { useState } from 'react';
import HotelCard from './HotelCard';

const Rating = ({ hotels, onSubmitRatings, onBack }) => {
  const [selectedHotel, setSelectedHotel] = useState('');
  const [currentRating, setCurrentRating] = useState(0);
  const [userRatings, setUserRatings] = useState({});

  const handleAddRating = () => {
    if (selectedHotel && currentRating > 0) {
      setUserRatings(prev => ({
        ...prev,
        [selectedHotel]: currentRating
      }));
      setSelectedHotel('');
      setCurrentRating(0);
    }
  };

  const handleRemoveRating = (hotelId) => {
    setUserRatings(prev => {
      const newRatings = { ...prev };
      delete newRatings[hotelId];
      return newRatings;
    });
  };

  const handleSubmit = () => {
    if (Object.keys(userRatings).length >= 5) {
      onSubmitRatings(userRatings);
    } else {
      alert('Veuillez noter au moins 5 hôtels');
    }
  };

  const availableHotels = hotels.filter(hotel => !userRatings[hotel.hotel_id]);

  return (
    <div className="rating-interface">
      <h1>NOTEZ VOS HÔTELS VISITÉS</h1>

      <div className="rating-form">
        <select
          value={selectedHotel}
          onChange={(e) => setSelectedHotel(e.target.value)}
        >
          <option value="">Choisissez un hôtel...</option>
          {availableHotels.map(hotel => (
            <option key={hotel.hotel_id} value={hotel.hotel_id}>
              🏨 {hotel.nom}
            </option>
          ))}
        </select>

        <div className="rating-input">
          {[1, 2, 3, 4, 5].map(star => (
            <span
              key={star}
              className={`star ${star <= currentRating ? 'filled' : ''}`}
              onClick={() => setCurrentRating(star)}
            >
              ⭐️
            </span>
          ))}
        </div>

        <button onClick={handleAddRating} disabled={!selectedHotel || currentRating === 0}>
          Ajouter Note
        </button>
      </div>

      <div className="rated-hotels">
        <h2>Vos notes ({Object.keys(userRatings).length}/5 minimum)</h2>
        {Object.entries(userRatings).map(([hotelId, rating]) => {
          const hotel = hotels.find(h => h.hotel_id === hotelId);
          return (
            <div key={hotelId} className="rated-hotel-item">
              <span>{hotel.nom}</span>
              <div className="rating-display">
                {[1, 2, 3, 4, 5].map(star => (
                  <span key={star} className={`star ${star <= rating ? 'filled' : ''}`}>
                    ⭐️
                  </span>
                ))}
                <span>({rating}/5)</span>
              </div>
              <button onClick={() => handleRemoveRating(hotelId)}>❌</button>
            </div>
          );
        })}
      </div>

      <button
        className="submit-button"
        onClick={handleSubmit}
        disabled={Object.keys(userRatings).length < 5}
      >
        [OBTENIR RECOMMANDATIONS]
      </button>

      <button className="back-button" onClick={onBack}>
        ← RETOUR À LA SÉLECTION
      </button>
    </div>
  );
};

export default Rating;