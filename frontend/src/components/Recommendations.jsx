import React from 'react';
import './Recommendations.css';

function Recommendations({ recommendations, onReset }) {
  // Defensive: ensure `recommendations` is an array to avoid runtime errors
  const recs = Array.isArray(recommendations) ? recommendations : [];

  return (
    <div className="recommendations-container">
      <div className="section-header">
        <h2>Étape 2: Vos recommandations personnalisées</h2>
        <p>Basées sur vos préférences et celles d'utilisateurs similaires</p>
      </div>

      {recs.length === 0 ? (
        <div className="no-recommendations">
          <p>Aucune recommandation disponible. Veuillez essayer avec d'autres évaluations.</p>
        </div>
      ) : (
        <div className="recommendations-grid">
          {recs.map((item, idx) => (
            <div key={idx} className="recommendation-card">
              <div className="rank">#{idx + 1}</div>
              <h3>{item.nom}</h3>
              <p className="category">{item.categorie} • {item.localisation}</p>
              <div className="prediction-score">
                <div className="score-label">Score prédit</div>
                <div className="score-value">{item.predicted_rating.toFixed(1)}/5</div>
                <div className="score-bar">
                  <div
                    className="score-fill"
                    style={{ width: `${(item.predicted_rating / 5) * 100}%` }}
                  />
                </div>
              </div>
              <p className="price">💰 {item.prix}</p>
              <p className="explanation">
                <small>Raison: {item.reason || 'Recommandé par utilisateurs similaires'}</small>
              </p>
            </div>
          ))}
        </div>
      )}

      <div className="action-buttons">
        <button className="btn btn-secondary" onClick={onReset}>
          ← Retour aux évaluations
        </button>
      </div>
    </div>
  );
}

export default Recommendations;
