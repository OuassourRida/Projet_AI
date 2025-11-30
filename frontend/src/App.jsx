import React, { useEffect, useState } from 'react'
import { hotelService, apiUtils } from './services/api'
import HotelCard from './components/HotelCard'
import Recommendations from './components/Recommendations'
import UserProfile from './components/UserProfile'
import './App.css'

export default function App() {
  const [hotels, setHotels] = useState([])
  const [loading, setLoading] = useState(true)
  const [userRatings, setUserRatings] = useState({})
  const [recommendations, setRecommendations] = useState([])
  const [error, setError] = useState(null)

  useEffect(() => {
    async function load() {
      try {
        const data = await hotelService.getAllHotels()
        // data may be an array or object depending on API; handle both
        setHotels(Array.isArray(data) ? data : data)
      } catch (e) {
        setError(apiUtils.formatError(e))
      } finally {
        setLoading(false)
      }
    }

    load()
  }, [])

  const handleRate = (hotelId, rating) => {
    setUserRatings((prev) => ({ ...prev, [hotelId]: rating }))
  }

  const handleRequestRecommendations = async () => {
    if (!userRatings || Object.keys(userRatings).length === 0) {
      setError('Veuillez noter au moins un hôtel avant de générer des recommandations.')
      return
    }

    try {
      setLoading(true)
      setError(null)
      const recs = await hotelService.getRecommendations(userRatings, 5)
      setRecommendations(Array.isArray(recs) ? recs : recs)
    } catch (e) {
      // show detailed message when available
      setError(apiUtils.formatError(e))
      setRecommendations([])
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="app-container">
      <header>
        <h1>Recommande-moi Marrakech — Hôtels</h1>
      </header>

      <main>
        <UserProfile onSubmitRatings={() => handleRequestRecommendations()} initialRatings={{}} />

        {error && <div className="error">{error}</div>}

        <section>
          <h2>Liste des hôtels</h2>
          {loading && <div>Chargement...</div>}

          {!loading && (
            <div className="hotels-grid">
              {hotels.map((h) => (
                <HotelCard key={h.hotel_id} hotel={h} onRate={handleRate} />
              ))}
            </div>
          )}
        </section>

        <section style={{ marginTop: 24 }}>
          <Recommendations recommendations={recommendations} />
        </section>

        <div style={{ marginTop: 24 }}>
          <button onClick={handleRequestRecommendations} disabled={!userRatings || Object.keys(userRatings).length === 0}>
            Générer recommandations
          </button>
          {!userRatings || Object.keys(userRatings).length === 0 ? (
            <div style={{ color: '#6b7280', marginTop: 8 }}>Notez au moins un hôtel pour activer le bouton.</div>
          ) : (
            <div style={{ color: '#6b7280', marginTop: 8 }}>{Object.keys(userRatings).length} hôtels notés</div>
          )}
        </div>
      </main>
    </div>
  )
}
