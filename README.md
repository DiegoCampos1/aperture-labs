# Aperture Labs - Employee Time Tracking

A full-stack monorepo application for tracking employee labour hours at Aperture Laboratories. Built with **Django REST Framework** (backend) and **Next.js** (frontend), orchestrated with **Docker Compose**.

## Tech Stack

### Backend
- Python 3.12, Django 5, Django REST Framework
- PostgreSQL 16
- Labour hours calculation engine (Morning / Afternoon / Evening / Late Night periods)

### Frontend
- Next.js 14 (App Router), TypeScript
- Material UI v6, Tailwind CSS
- React Query (TanStack Query v5), Axios
- Responsive design: Desktop (4-col grid), Tablet (2-col), Mobile (1-col)

## Getting Started

### Prerequisites
- [Docker](https://www.docker.com/) and Docker Compose installed

### Run the project

```bash
# From the aperture-labs directory
docker compose up --build
```

This will start:
- **PostgreSQL** on port `5432`
- **Django API** on [http://localhost:8000](http://localhost:8000)
- **Next.js App** on [http://localhost:3000](http://localhost:3000)

The database is automatically migrated and seeded with the Aperture Labs employee clock data on first startup.

### API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/employees/` | List all employees with total hours |
| GET | `/api/employees/?search=cave` | Filter employees by name |
| GET | `/api/employees/{id}/labour/` | Detailed labour breakdown by date |

### Running Tests

```bash
# Backend tests
docker compose exec backend python manage.py test

# Or without Docker (requires PostgreSQL running)
cd backend
python manage.py test
```

## Architecture Decisions

1. **Server-side filtering**: The search/filter feature sends requests to the Django backend, which queries PostgreSQL with case-insensitive partial matching on first and last names.

2. **Labour hours calculation**: Shifts are split across 4 time periods (Morning 5AM-12PM, Afternoon 12PM-6PM, Evening 6PM-11PM, Late Night 11PM-5AM). Multi-day shifts are handled by iterating day-by-day through ordered period boundaries.

3. **Data seeding via migrations**: The initial employee and clock data is loaded through a Django data migration (`0002_seed_data.py`), ensuring the database is populated automatically on first `migrate`.

4. **Skeleton loading states**: The frontend shows animated skeleton cards while waiting for API responses, providing visual feedback during data fetching.

5. **Debounced search**: Filter input has a 300ms debounce to avoid excessive API calls while typing.
