/**
 * Service API pour communiquer avec le backend FastAPI
 * Gère les appels pour les hôtels et les recommandations
 */

import axios from 'axios'

// URL de base de l'API FastAPI
const API_BASE_URL = 'http://127.0.0.1:8000/api'

// Configuration de l'instance Axios
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
    timeout: 20000, // 20 secondes de timeout
})

// Intercepteur pour gérer les erreurs globalement
api.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error('Erreur API:', error.response?.data || error.message)
    return Promise.reject(error)
  }
)

/**
 * Service pour les opérations liées aux hôtels
 */
export const hotelService = {
  /**
   * Récupère tous les hôtels disponibles
   * @returns {Promise<Array>} Liste des hôtels
   */
  getAllHotels: async () => {
    try {
      const response = await api.get('/hotels')
      return response.data
    } catch (error) {
      console.error('Erreur lors de la récupération des hôtels:', error)
      throw new Error('Impossible de récupérer les hôtels. Vérifiez que le serveur est démarré.')
    }
  },

  /**
   * Récupère les détails d'un hôtel spécifique
   * @param {number} hotelId - ID de l'hôtel
   * @returns {Promise<Object>} Détails de l'hôtel
   */
  getHotelById: async (hotelId) => {
    try {
      const response = await api.get(`/hotels/${hotelId}`)
      return response.data
    } catch (error) {
      console.error(`Erreur lors de la récupération de l'hôtel ${hotelId}:`, error)
      throw new Error(`Impossible de récupérer les détails de l'hôtel ${hotelId}`)
    }
  },

  /**
   * Génère des recommandations personnalisées
   * @param {Object} userRatings - Ratings de l'utilisateur {hotel_id: rating}
   * @param {number} nRecommendations - Nombre de recommandations désirées
   * @returns {Promise<Array>} Liste des recommandations
   */
  getRecommendations: async (userRatings, nRecommendations = 5) => {
    try {
      const requestData = {
        user_ratings: userRatings,
        n_recommendations: nRecommendations
      }
      
      const response = await api.post('/recommend', requestData)
      return response.data
    } catch (error) {
      console.error('Erreur lors de la génération des recommandations:', error)
      
      if (error.response?.status === 400) {
        throw new Error('Données de notation invalides. Veuillez noter au moins un hôtel.')
      }
      
      throw new Error('Impossible de générer des recommandations. Veuillez réessayer.')
    }
  },

  /**
   * Version simplifiée pour obtenir des recommandations
   * @param {Object} userRatings - Ratings de l'utilisateur
   * @returns {Promise<Object>} Recommandations avec métadonnées
   */
  getSimpleRecommendations: async (userRatings) => {
    try {
      const response = await api.post('/recommend/simple', userRatings)
      return response.data
    } catch (error) {
      console.error('Erreur lors des recommandations simples:', error)
      throw new Error('Impossible de générer des recommandations')
    }
  },

  /**
   * Récupère les statistiques du système
   * @returns {Promise<Object>} Statistiques générales
   */
  getSystemStats: async () => {
    try {
      const response = await api.get('/stats')
      return response.data
    } catch (error) {
      console.error('Erreur lors de la récupération des statistiques:', error)
      throw new Error('Impossible de récupérer les statistiques')
    }
  },

  /**
   * Vérifie l'état de santé de l'API
   * @returns {Promise<Object>} Status de l'API
   */
  checkHealth: async () => {
    try {
      const response = await api.get('/health')
      return response.data
    } catch (error) {
      console.error('Erreur lors de la vérification de santé:', error)
      throw new Error('API indisponible')
    }
  }
}

/**
 * Utilitaires pour la gestion des erreurs
 */
export const apiUtils = {
  /**
   * Formate les erreurs pour l'affichage utilisateur
   * @param {Error} error - Erreur à formater
   * @returns {string} Message d'erreur formaté
   */
  formatError: (error) => {
    if (error.response?.data?.detail) {
      return error.response.data.detail
    }
    return error.message || 'Une erreur inattendue s\'est produite'
  },

  /**
   * Vérifie si l'API est accessible
   * @returns {Promise<boolean>} True si l'API est accessible
   */
  isApiAvailable: async () => {
    try {
      await hotelService.checkHealth()
      return true
    } catch {
      return false
    }
  }
}

export default api