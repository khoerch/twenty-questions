.PHONY: install-frontend install-backend start-frontend start-backend start

# Frontend commands
install-frontend:
	cd frontend && npm install

start-frontend:
	cd frontend && npm start

# Backend commands
install-backend:
	cd backend && \
	python -m venv venv && \
	. venv/bin/activate && \
	pip install -r requirements.txt

start-backend:
	cd backend && \
	. venv/bin/activate && \
	python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Combined commands
install: install-frontend install-backend

start:
	@echo "Starting both frontend and backend services..."
	@echo "Backend will run on http://localhost:8000"
	@echo "Frontend will run on http://localhost:3000"
	@make start-backend & make start-frontend