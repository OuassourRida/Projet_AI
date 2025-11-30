import React, { useState } from 'react'
import './HotelCard.css'

// Composant pour afficher un hôtel et permettre la notation
export default function HotelCard({ hotel, onRate }) {
  const [rating, setRating] = useState(0)
  const [justRated, setJustRated] = useState(false)

  const handleRate = (value) => {
    setRating(value)
    setJustRated(true)
    if (onRate) onRate(hotel.hotel_id, value)
    setTimeout(() => setJustRated(false), 600)
  }

  return (
    <div className="hotel-card">
      <div className="hotel-card-header">
        <h3 className="hotel-name">{hotel.nom}</h3>
        <div className="hotel-category">{hotel.categorie}</div>
      </div>

      <div className="hotel-info">
        <div className="hotel-info-item">
          <div className="hotel-info-icon">📍</div>
          <div>
            <div className="hotel-location">{hotel.localisation}</div>
            <div className="average-rating">Moyenne: {hotel.avg_rating ?? '-'} ⭐</div>
          </div>
        </div>

        <div className="hotel-info-item">
          <div className="hotel-info-icon">💶</div>
          <div className="hotel-price">{hotel.prix} MAD</div>
        </div>
      </div>

      <div className="hotel-amenities">
        <div className="amenities-title">Commodités</div>
        <div className="amenities-list">
          {(hotel.commodites || '').split(',').slice(0, 6).map((a, idx) => (
            <div className="amenity-tag" key={idx}>{a.trim()}</div>
          ))}
        </div>
      </div>

      <div className="rating-section">
        <div className="rating-label">Noter cet hôtel</div>
        <div className={`rating-stars ${justRated ? 'just-rated' : ''}`}>
          {[1, 2, 3, 4, 5].map((s) => (
            <button
              key={s}
              className={`star-btn ${s <= rating ? 'filled' : ''} ${justRated && s === rating ? 'just-rated' : ''}`}
              onClick={() => handleRate(s)}
              aria-label={`Noter ${s} étoiles`}
              title={`Noter ${s} étoiles`}
            >
              <svg className="star-icon" viewBox="0 0 24 24" width="20" height="20" aria-hidden="true">
                <path d="M12 .587l3.668 7.431 8.2 1.192-5.934 5.788 1.402 8.172L12 18.896l-7.336 3.874 1.402-8.172L.132 9.21l8.2-1.192z" />
              </svg>
            </button>
          ))}
          <span className="rating-display current-rating">{rating > 0 ? `${rating}.0` : '—'}</span>
        </div>
      </div>
    </div>
  )
}
