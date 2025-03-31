# Twenty Questions Game

A simple 20 Questions game where users try to guess a daily noun by asking yes/no questions.

## Project Structure

- `frontend/`: React frontend application
- `backend/`: FastAPI backend service

## Setup and Installation

### Prerequisites

- Node.js
- Python
- npm or yarn
- make (Required for running Makefile commands)

### Installing Make

#### macOS
1. Using Homebrew (recommended):
```bash
brew install make
```

2. Using Xcode Command Line Tools:
```bash
xcode-select --install
```

#### Windows
1. Using Chocolatey (recommended):
```bash
choco install make
```

2. Using Windows Subsystem for Linux (WSL):
- Install WSL from Microsoft Store
- Then install make within WSL:
```bash
sudo apt-get update
sudo apt-get install make
```

3. Using Git Bash:
- Make comes pre-installed with Git for Windows
- Download from: https://gitforwindows.org/

#### Linux
- Ubuntu/Debian:
```bash
sudo apt-get update
sudo apt-get install make
```
- Fedora:
```bash
sudo dnf install make
```
- CentOS/RHEL:
```bash
sudo yum install make
```

### Verifying Installation
To verify make is installed correctly:
```bash
make --version
```

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

- Frontend will be available at: http://localhost:3000
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

## Future Improvements

1. Create the SuccessModal component for when users win
2. Create the HintPanel component
3. Set up the backend API for question evaluation
    - Added a FastAPI backend, but it's a very basic implementation. 
4. Implement the LLM integration for processing questions
    - Consider caching and rate limiting to avoid high costs
    - Rate limiting was added
    - Caching was added but not working currently. I should consider caching specific functions instead of endpoints. 
5. Create a daily answer system
    - Added a daily answer system!
    - A scheduler runs daily to generate a new answer
6. Add local storage for maintaining game state