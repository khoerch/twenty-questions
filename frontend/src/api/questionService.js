const API_URL = 'http://localhost:8000/api';

export const evaluateQuestion = async (question) => {
  try {
    const response = await fetch(`${API_URL}/questions/evaluate`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ text: question }),
    });
    
    if (!response.ok) {
      throw new Error('Failed to evaluate question');
    }
    
    return await response.json();
  } catch (error) {
    console.error('Error evaluating question:', error);
    throw error;
  }
}; 