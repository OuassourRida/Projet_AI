import React from 'react'
import './HotelCard.css'

// Affiche la liste des recommandations
export default function Recommendations({ recommendations }) {
  if (!recommendations || recommendations.length === 0) {
    return <div>Aucune recommandation disponible.</div>
  }

  return (
    <div>
      <h2>Recommandations pour vous</h2>
      <div>
        {recommendations.map((r) => (
          <div key={r.hotel_id} style={{ padding: '12px', borderBottom: '1px solid #eee' }}>
            <h3 style={{ margin: 0 }}>{r.nom} — {r.predicted_rating} <span style={{ color: '#fbbf24' }}>★</span></h3>
            <div style={{ color: '#6b7280', marginTop: 6 }}>{r.localisation} • {r.categorie} • {r.prix} MAD</div>
            <p style={{ marginTop: 8 }}>{r.explanation || r.reason || 'Recommandé par des utilisateurs similaires'}</p>

            {/* Affiche les commodités si présentes */}
            {(r.commodites || r.amenities || '').toString().trim() !== '' && (
              <div style={{ marginTop: 8 }}>
                <div style={{ fontSize: '0.9rem', fontWeight: 600, color: '#374151', marginBottom: 6 }}>Commodités</div>
                <div className="amenities-list">
                  {( (r.commodites || r.amenities || '') .toString().split(',').slice(0, 8)).map((a, idx) => (
                    <div className="amenity-tag" key={idx}>{a.trim()}</div>
                  ))}
                </div>
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  )
}