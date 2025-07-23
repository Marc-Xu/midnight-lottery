# Midnight Lottery

**Midnight Lottery** is a FastAPI application that allows users to participate in lotteries. It features a layered architecture (Router → Service → Repository → ORM → Database), custom error handling, and full test coverage.

## Features

- Environment-based configuration via `.env`
- SQLAlchemy 2.0 ORM with typed models
- Repository layer with generic and specialized methods
- Service layer enforcing business rules
- Clean API routing using FastAPI routers
- Custom exceptions and global handlers
- CI pipelines for linting and testing on PRs to `main`

## Getting Started

### Prerequisites

- Python 3.12+
- [Poetry](https://python-poetry.org/) for dependency management

### Installation

1. Clone the repository:
   ```bash
   git clone git@github.com:Marc-Xu/midnight-lottery.git
   cd midnight-lottery
   ```
2. Install dependencies:
   ```bash
   poetry install
   ```

### Running the App

#### Locally
```bash
uvicorn app.main:app --reload
```
The API will be available at `http://localhost:8000`.

## API Endpoints

### Health Check
```
GET /health
Response: { "status": "ok" }
```

### Participants
```
POST   /participants/               Create a new participant
GET    /participants/               List participants (skip, limit)
GET    /participants/{id}           Retrieve by ID
PATCH  /participants/{id}           Partially update
DELETE /participants/{id}           Delete by ID
```

### Draws
```
POST   /draws/               Create a new draw
GET    /draws/               List draws (skip, limit)
GET    /draws/daily-draw     Draw or retrieve a winner
GET    /draws/{id}           Retrieve by ID
DELETE /draws/{id}           Delete by ID
```

### Ballots
```
POST    /ballots/               Create a new ballot
GET     /ballots/               List ballots (skip, limit)
GET     /ballots/{id}           Retrieve by ID
DELETE  /ballots/{id}           Delete by ID
```

## Testing

Run the full pytest suite:
```bash
pytest --maxfail=1 --disable-warnings -q
```

Tests spin up an in-memory SQLite database per test for isolation.

## CI & Deployment

- **GitHub Actions** workflows in `.github/workflows/`
  - `ci.yml` runs Black, Ruff, and pytest on pull requests.
  - `release.yml` automatically bumps the patch version on `main` merges.
- **Docker** support via the provided `Dockerfile`.

## Contributing

1. Fork the repo and create a feature branch.
2. Write tests for your changes.
3. Ensure linting and tests pass locally.
4. Open a pull request; CI will validate your changes.