import React, { useState } from 'react'

// Composant simple pour gérer le profil utilisateur et ses ratings
export default function UserProfile({ onSubmitRatings, initialRatings = {} }) {
  const [ratings, setRatings] = useState(initialRatings)

  const handleChange = (hotelId, value) => {
    setRatings((prev) => ({ ...prev, [hotelId]: Number(value) }))
  }

  const handleSubmit = (e) => {
    e.preventDefault()
    if (onSubmitRatings) onSubmitRatings(ratings)
  }

  return (
    <form onSubmit={handleSubmit} style={{ marginBottom: 20 }}>
      <h2>Votre profil & notes</h2>
      <p>Notez quelques hôtels pour obtenir des recommandations personnalisées (5-10 recommandés).</p>

      {/* In real app we'd render inputs for selected hotels; here we provide a submit button */}
      <div style={{ marginTop: 12 }}>
        <button type="submit">Obtenir des recommandations</button>
      </div>
    </form>
  )
}
