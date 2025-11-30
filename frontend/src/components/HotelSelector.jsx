import React, { useState } from 'react';

const HotelSelector = ({ hotels, onHotelSelection }) => {
  const [selectedHotels, setSelectedHotels] = useState([]);
  const [searchTerm, setSearchTerm] = useState('');

  const filteredHotels = hotels.filter(hotel =>
    hotel.nom.toLowerCase().includes(searchTerm.toLowerCase()) &&
    !selectedHotels.find(selected => selected.hotel_id === hotel.hotel_id)
  );

  const handleAddHotel = (hotel) => {
    if (selectedHotels.length < 10) {
      setSelectedHotels([...selectedHotels, hotel]);
    }
  };

  const handleRemoveHotel = (hotelId) => {
    setSelectedHotels(selectedHotels.filter(hotel => hotel.hotel_id !== hotelId));
  };

  const handleSubmit = () => {
    if (selectedHotels.length >= 5) {
      onHotelSelection(selectedHotels);
    }
  };

  return (
    <div className="hotel-selector">
      <h1>SÉLECTIONNEZ LES HÔTELS QUE VOUS AVEZ DÉJÀ VISITÉS</h1>
      <p>Choisissez 5 à 10 hôtels que vous avez déjà visités pour recevoir des recommandations personnalisées.</p>

      <div className="search-section">
        <input
          type="text"
          placeholder="Rechercher un hôtel..."
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          className="search-input"
        />
        <div className="hotel-dropdown">
          {filteredHotels.slice(0, 5).map(hotel => (
            <div
              key={hotel.hotel_id}
              className="hotel-option"
              onClick={() => handleAddHotel(hotel)}
            >
              🏨 {hotel.nom} - {hotel.localisation} ({hotel.categorie})
            </div>
          ))}
        </div>
      </div>

      <div className="selected-hotels">
        <h3>Hôtels sélectionnés ({selectedHotels.length}/10):</h3>
        {selectedHotels.map(hotel => (
          <div key={hotel.hotel_id} className="selected-hotel">
            <span>🏨 {hotel.nom}</span>
            <button
              onClick={() => handleRemoveHotel(hotel.hotel_id)}
              className="remove-btn"
            >
              ❌
            </button>
          </div>
        ))}
      </div>

      <button
        className="submit-button"
        onClick={handleSubmit}
        disabled={selectedHotels.length < 5}
      >
        COMMENCER À NOTER CES HÔTELS ({selectedHotels.length})
      </button>
    </div>
  );
};

export default HotelSelector;