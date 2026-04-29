# Banyu Guide - ML Recommendation Service

Python-based ML service untuk sistem rekomendasi wisata dan kuliner Banyuwangi.

## Tech Stack
- **FastAPI** - Web framework
- **scikit-learn** - ML algorithms (Collaborative Filtering)
- **pandas** - Data processing

## Setup

```bash
# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy env file
copy .env.example .env
```

## Run Development Server

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8001
```

## API Documentation
- Swagger UI: `http://localhost:8001/docs`
- ReDoc: `http://localhost:8001/redoc`

## Project Structure
```
ml_service/
├── app/
│   ├── main.py              # FastAPI entry point
│   ├── config.py            # Configuration
│   ├── api/                 # API routes & schemas
│   ├── core/                # Data loader & preprocessor
│   ├── recommenders/        # Recommender classes
│   ├── notebooks/           # Training notebooks
│   └── utils/               # Helper functions
└── artifacts/               # Trained models & data
    ├── models/              # .pkl files
    └── data/                # CSV files
```
