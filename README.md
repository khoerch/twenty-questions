# Twenty Questions Game

A simple 20 Questions game where users try to guess a daily noun by asking yes/no questions.

## Project Structure

- `frontend/`: React frontend application
- `backend/`: FastAPI backend service

## Setup and Installation

### Prerequisites

- Node.js (v14+)
- Python (v3.8+)
- npm or yarn

### Installation

1. Clone the repository
2. Install dependencies:

```bash
# Install all dependencies
make install
# Or install separately
make install-frontend
make install-backend
```

### Running the Application

```bash
# Start both frontend and backend
make start
# Start frontend only
make start-frontend
# Start backend only
make start-backend
```

- Frontend will be available at: http://localhost:8080
- Backend will be available at: http://localhost:8000

## Game Rules

1. Every day, there is a new noun or proper noun to guess
2. Users have 20 yes/no questions to figure out the answer
3. Users can use up to 3 hints per day
4. Questions are evaluated for relevance (indicated by 🔥 for high relevance or ❄️ for low relevance)

## Development

### Frontend

The frontend is built with React and uses Emotion for styling. The UI is designed to be simple and intuitive, inspired by Wordle and similar games.

### Backend

The backend is built with FastAPI and uses LLMs for question evaluation. The API provides endpoints for:
- Evaluating yes/no questions
- Retrieving hints
- Checking if an answer is correct

## Project Structure

```bash
twenty-questions/
├── frontend/ # React frontend
│ ├── public/ # Static files
│ ├── src/ # Source code
│ │ ├── components/ # React components
│ │ └── App.js # Main application component
│ ├── package.json # Frontend dependencies
│ └── webpack.config.js # Webpack configuration
├── backend/ # FastAPI backend
│ ├── main.py # Main application file
│ └── requirements.txt # Python dependencies
├── Makefile # Commands for running the application
└── README.md # Project documentation
```