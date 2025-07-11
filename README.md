# ServiceApp

This repository contains a small service marketplace application with a Flask backend and a React frontend.

## Local Development

### Backend
1. Install dependencies:
   ```bash
   cd servicios-backend
   python3 -m venv venv
   source venv/bin/activate
   pip install -r ../requirements.txt
   ```
2. Configure environment variables in `.env` or your shell:
   - `SECRET_KEY` – secret string for Flask sessions (default `change-me`)
   - `DATABASE_URI` – SQLAlchemy database URI (defaults to a local SQLite database)
3. Start the development server:
   ```bash
   python src/main.py
   ```
   The API will be available on <http://localhost:5000>.

### Frontend
1. Install dependencies:
   ```bash
   cd servicios-app
   npm install
   ```
2. Optionally set `REACT_APP_API_URL` to override the backend URL (defaults to `/api`).
3. Launch the Vite dev server:
   ```bash
   npm run dev
   ```
   The app will open on <http://localhost:5173> and will proxy API requests to the backend.

## Deployment on Render

The repository includes a [`render.yaml`](render.yaml) describing two services:

- **servi-app-backend** – Python web service built with `pip install -r requirements.txt` and started using `gunicorn src.main:app`.
- **servi-app-frontend** – Static site built with `npm install && npm run build` and served from the `dist` directory.

Create a new Render Blueprint and point it at this repository to provision both services automatically.

## Environment Variables

These variables are used by the application:

| Variable | Description | Default |
|----------|-------------|---------|
| `SECRET_KEY` | Flask secret key | `change-me` |
| `DATABASE_URI` | SQLAlchemy database URI | `sqlite:///src/database/app.db` |
| `FLASK_APP` | Entry point for Flask (Render) | `src/main.py` |
| `FLASK_ENV` | Flask environment (Render) | `production` |
| `REACT_APP_API_URL` | Frontend base URL for the API | `/api` |

Define them in Render or in local `.env` files as needed.
