import './HotelCard.css'

export default function HotelCard({ hotel }) {
  // hotel can be a string or object
  const title = typeof hotel === 'string' ? hotel : hotel.name || hotel.title || hotel.id || 'Hôtel'
  const desc = typeof hotel === 'object' && (hotel.description || hotel.desc || hotel.address)

  return (
    <div className="hotel-card">
      <div className="hotel-title">{title}</div>
      {desc && <div className="hotel-desc">{desc}</div>}
    </div>
  )
}
