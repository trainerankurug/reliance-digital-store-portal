# Reliance Digital – Store Operations Portal

A small starter repository for the Reliance Digital case study. It provides a product catalogue and inventory view that can be extended by a development team using an AI coding assistant.

## Technology stack
- Backend: Python 3.11+, FastAPI
- Frontend: React 18, Vite, JavaScript
- Tests: pytest

## Repository layout
```text
reliance-digital-store-portal/
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── models.py
│   │   └── services/
│   │       └── product_service.py
│   ├── tests/
│   │   └── test_products.py
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── App.jsx
│   │   ├── api.js
│   │   └── main.jsx
│   ├── index.html
│   └── package.json
└── README.md
```

## Run the backend
```bash
cd backend
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```
API: http://127.0.0.1:8000  
API docs: http://127.0.0.1:8000/docs

## Inventory monitoring agent
The read-only `GET /api/agents/inventory-monitoring` endpoint returns stock totals, product lists by status, and manager-attention recommendations. It analyzes active products only: zero stock is out of stock, 1–4 is low stock, and 5 or more is normal stock. The report excludes product prices and does not call an external LLM.

The GitHub Copilot custom agent is defined in `.github/agents/reliance-digital-inventory-monitoring.agent.md`. It runs the local report generator, which writes product-level recommendations to a temporary JSON file and prints only aggregate counts for the LLM.

The current sample inventory can be tested by starting the backend and requesting:
```bash
curl http://127.0.0.1:8000/api/agents/inventory-monitoring
```

Focused tests use synthetic inventory values:
```bash
cd backend
pytest tests/test_inventory_monitoring_agent.py
```

## README freshness workflow
The GitHub Agentic Workflow in `.github/workflows/readme-freshness.md` checks whether changes on `main` leave the root README inaccurate or missing important setup or behavior. It runs on pushes to `main`, every day at 6:00 PM Pacific Time, and can be started manually from the GitHub Actions page with **Run workflow**. Verified documentation gaps are reported as GitHub issues; the workflow does not modify repository files.

## Run the frontend
In a second terminal:
```bash
cd frontend
npm install
npm run dev
```
Open the URL printed by Vite (normally http://localhost:5173).

## Run backend tests
```bash
cd backend
pytest
```

## Current functionality
- List products
- View a product by ID
- Search products by name
- View low-stock products

## Case-study extension
The development team wants AI-assisted changes to follow consistent repository conventions, project-specific expectations, quality practices, and safe-change boundaries. Use this repository to inspect the existing application and establish a consistent approach before asking the coding assistant to implement a new feature.

Do not assume that every future project will use this technology stack. The practices you establish should be adaptable to other languages and frameworks.
