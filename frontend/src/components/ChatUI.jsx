import { useState } from 'react'
import './ChatUI.css'
import HotelCard from './HotelCard'
import { getRecommendations } from '../services/api'

export default function ChatUI() {
  const [slots, setSlots] = useState(['', '', '', ''])
  const [messages, setMessages] = useState([])
  const [loading, setLoading] = useState(false)

  function setSlotValue(index, value) {
    const copy = [...slots]
    copy[index] = value
    setSlots(copy)
  }

  async function handleSend() {
    const nonEmpty = slots.map(s => s.trim()).filter(s => s)
    if (nonEmpty.length === 0) return
    setMessages(prev => [...prev, { from: 'user', text: `Asking for: ${nonEmpty.join(', ')}` }])
    setLoading(true)
    try {
      const resp = await getRecommendations(nonEmpty)
      // expecting resp.recommendations as array
      const recs = resp?.recommendations || resp || []
      setMessages(prev => [...prev, { from: 'bot', recommendations: recs }])
    } catch (err) {
      setMessages(prev => [...prev, { from: 'bot', text: 'Erreur: impossible de joindre le backend.' }])
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="chat-root">
      <aside className="chat-sidebar">
        <h2>Hotel Assistant</h2>
        <p>Entrez jusqu'à 4 hôtels (nom ou id) puis cliquez sur «Obtenir recommandations».</p>
        <div className="slots">
          {slots.map((s, i) => (
            <input
              key={i}
              className="slot-input"
              placeholder={`Hôtel ${i + 1}`}
              value={s}
              onChange={e => setSlotValue(i, e.target.value)}
            />
          ))}
        </div>
        <button className="send-btn" onClick={handleSend} disabled={loading}>
          {loading ? 'Chargement...' : 'Obtenir recommandations'}
        </button>
      </aside>

      <main className="chat-main">
        <div className="messages">
          {messages.length === 0 && <div className="empty">Les recommandations apparaîtront ici.</div>}
          {messages.map((m, idx) => (
            <div key={idx} className={`message ${m.from}`}>
              {m.from === 'user' && <div className="message-text">{m.text}</div>}
              {m.from === 'bot' && (
                <div>
                  {m.text && <div className="message-text">{m.text}</div>}
                  {Array.isArray(m.recommendations) && (
                    <div className="recommendations-list">
                      {m.recommendations.map((h, i) => (
                        <HotelCard key={i} hotel={h} />
                      ))}
                    </div>
                  )}
                </div>
              )}
            </div>
          ))}
        </div>
      </main>
    </div>
  )
}
