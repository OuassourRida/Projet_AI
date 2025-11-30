import React from 'react';
import './HotelCard.css';

function HotelCard({ hotel, rating, onRatingChange }) {
  return (
    <div className="hotel-card">
      <div className="hotel-header">
        <h3 className="hotel-name">{hotel.nom}</h3>
        <div className="hotel-meta">
          <span className="category">{hotel.categorie}</span>
          <span className="location">{hotel.localisation}</span>
        </div>
      </div>

      <div className="hotel-details">
        <p className="price">{hotel.prix}</p>
        <p className="stars">⭐ {hotel.etoiles}/5</p>
      </div>

      {hotel.commodites && (
        <p className="commodities">
          <small>{hotel.commodites}</small>
        </p>
      )}

      <div className="rating-section">
        <label>Votre note:</label>
        <div className="stars-input">
          {[1, 2, 3, 4, 5].map(star => (
            <button
              key={star}
              className={`star-btn ${rating >= star ? 'active' : ''}`}
              onClick={() => onRatingChange(hotel.hotel_id, star)}
              title={`${star} étoile${star > 1 ? 's' : ''}`}
            >
              ⭐
            </button>
          ))}
        </div>
        <span className="rating-value">{rating > 0 ? `${rating}/5` : 'Non noté'}</span>
      </div>
    </div>
  );
}

export default HotelCard;