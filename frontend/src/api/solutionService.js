const API_URL = 'http://localhost:8000/api';

export const getTodaysHint = async () => {
  try {
    const response = await fetch(`${API_URL}/solutions/current/hint`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
    });
    
    if (!response.ok) {
      throw new Error('Failed to fetch hint');
    }
    
    return await response.json();
  } catch (error) {
    console.error('Error fetching hint:', error);
    throw error;
  }
}; 