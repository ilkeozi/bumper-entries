# Guestbook API

![Build](https://github.com/ilkeozi/bumper-entries/actions/workflows/build.yml/badge.svg)
![Unit Tests](https://github.com/ilkeozi/bumper-entries/actions/workflows/unit-tests.yml/badge.svg)
![E2E and Integration Tests](https://github.com/ilkeozi/bumper-entries/actions/workflows/e2e-integration-tests.yml/badge.svg)

A Django RESTful API for a Guestbook application. This backend handles user entries, allowing users to create, retrieve, and delete entries. It supports pagination and optimized querying for efficient performance, with comprehensive test coverage and API documentation via Swagger.

## Features

- **User and Entry Management**: Create and manage guestbook users and their entries.

- **Automatic User Creation**: Automatically creates a new user if the `name` is unique when creating an entry.

- **Pagination and Ordering**: Retrieve entries with pagination in descending order by created date.

- **User Data Overview**: Displays total message count and latest entry details for each user.

- **Error Handling and Validation**: Structured error responses with validations on all input fields.

- **Optimized ORM Queries**: Advanced querying with Django ORM for better performance on larger datasets.

- **API Documentation**: Self-documenting API using Swagger (drf-yasg).

- **Comprehensive Testing**: Unit tests, integration tests, and E2E tests included.

## Technologies Used

- **Backend Framework**: Django with Django REST Framework (DRF)

- **Database**: PostgreSQL

- **API Documentation**: Swagger via drf-yasg

- **Testing**: Pytest, pytest-django, requests

- **Environment Management**: Python-dotenv for environment variables

## Getting Started

### Prerequisites

- Python 3.10+

- PostgreSQL

- pip package manager

- (Optional) `virtualenv` for isolated environment setup

### Installation

1.  **Clone the repository**:

```bash

git clone <repository-url>

cd bumper-entries
```

2.  **Set up a virtual environment**:

```bash
python3 -m venv myenv

source myenv/bin/activate
```

3.  **Install dependencies**:

```bash
pip install -r requirements.txt
```

4.  **Environment Variables**:
    Copy .env.example to .env and update the database credentials and other settings.

**Example .env file**:

```env
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_NAME=your_db_name
DB_HOST=your_db_hostname
DB_PORT=5432
```

4.  **Apply migrations**:

```bash
python manage.py migrate
```

5.  **Run the server**:

```bash
python manage.py runserver
```

## API Endpoints

The following endpoints are available:

| Endpoint             | Method | Description                        |
| -------------------- | ------ | ---------------------------------- |
| `/api/users/`        | POST   | Create a new user                  |
| `/api/users/`        | GET    | Retrieve all users                 |
| `/api/entries/`      | POST   | Create a new entry                 |
| `/api/entries/`      | GET    | Retrieve paginated list of entries |
| `/api/entries/{id}/` | GET    | Retrieve a single entry by ID      |
| `/api/entries/{id}/` | PUT    | Update an entry by ID              |
| `/api/entries/{id}/` | DELETE | Delete an entry by ID              |

## API Documentation

Swagger documentation is available at:

```arduino
http://127.0.0.1:8000/swagger/
```

## Testing

This project includes unit tests, integration tests, and E2E tests.

**Run all tests**:

```bash
pytest --reuse-db
```

**Run unit tests**:

```bash
pytest guestbook/tests/unit/
```

**Run integration tests**:

```bash
pytest guestbook/tests/integration/
```

**Run E2E tests:**

```bash
pytest --reuse-db guestbook/tests/e2e/
```

## Project Structure

- **guestbook**: Contains the main app code including models, views, serializers, and services.
- **api**: API endpoints and serializers
- **services**: Business logic and database interaction
- **schemas**: DTOs and validation logic
- **tests**: Contains unit, integration, and E2E tests
