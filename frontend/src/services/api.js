export async function getRecommendations(hotels) {
	// hotels: array of hotel identifiers or names
	try {
		const res = await fetch('http://localhost:5000/recommendations', {
			method: 'POST',
			headers: { 'Content-Type': 'application/json' },
			body: JSON.stringify({ hotels }),
		})
		if (!res.ok) {
			throw new Error('Network response was not ok')
		}
		const data = await res.json()
		return data
	} catch (err) {
		// Fallback: return a mocked response so frontend remains usable without backend
		console.warn('API call failed, returning mock recommendations.', err)
		return {
			recommendations: hotels.slice(0, 3).map((h, i) => ({ id: i + 1, name: `Recommandation pour ${h}` })),
		}
	}
}
