# TaskFlow API

A REST API for a small team task manager, built with Django and Django REST Framework.
Users can create projects, manage tasks with assignees, and comment on tasks — with
role-based access control, JWT authentication, filtering, and interactive documentation.

---

## Tech Stack

- **Python** 3.12+
- **Django** 5.x
- **Django REST Framework** — REST API
- **PostgreSQL** 16 — database
- **djangorestframework-simplejwt** — JWT authentication
- **drf-spectacular** — OpenAPI 3.0 schema + Swagger UI
- **django-filter** — filtering
- **pytest** + **pytest-django** — testing
- **Docker** + **Docker Compose** — containerized development

---

## Features

### Core
- **Projects** — CRUD, owned by a single user (`owner`), unique name per owner
- **Tasks** — CRUD, belong to a project, can have multiple assignees (M2M)
- **Comments** — CRUD, belong to a task, authored by a user
- **Custom User model** — `AbstractUser` (ready for future extension)

### Access control
- **JWT authentication** — `access` + `refresh` tokens
- **Owner isolation** — users only see their own projects
- **Task visibility** — project owner **or** assignee can view a task
- **Role-based editing**:
  - **Project owner** — full CRUD on the project and its tasks
  - **Task assignee** — can only change the task's `status`
  - **Comment author** — can only edit their own comments
- **404 on foreign objects** — no information leakage (a foreign resource looks "not found")

### API features
- **Pagination** — `PageNumberPagination` (10 items per page)
- **Filtering** — `?status=todo`, `?priority=high`, `?project=1`, `?task=1`, `?author=1`
- **Search** — `?search=...` on titles, descriptions, names, comment texts
- **Ordering** — `?ordering=due_date`, `?ordering=-created_at`
- **Validation** — `due_date` cannot be in the past on creation; assignees only edit `status`
- **Interactive docs** — Swagger UI at `/api/docs/`

---

## Getting Started

### Prerequisites

- Python 3.12+
- PostgreSQL 16 (or Docker)

### Option A — Local setup

    git clone <repo-url> taskflow
    cd taskflow

    python -m venv .venv
    source .venv/bin/activate        # Linux / macOS
    # .venv\Scripts\activate         # Windows

    pip install -r requirements.txt

    cp .env.example .env
    # Edit .env and set SECRET_KEY, DATABASE_URL, etc.

    python manage.py migrate

    python manage.py createsuperuser

    python manage.py runserver

Open:
- **Swagger UI** — http://127.0.0.1:8000/api/docs/
- **Django Admin** — http://127.0.0.1:8000/admin/
- **API root** — http://127.0.0.1:8000/api/

### Option B — Docker Compose

    git clone <repo-url> taskflow
    cd taskflow

    cp .env.example .env
    # Set DATABASE_URL=postgres://taskflow:taskflow@db:5432/taskflow
    # (note: "db" is the service name inside Docker, not "localhost")

    docker-compose up --build

    # In another terminal — apply migrations and create a superuser
    docker-compose exec web python manage.py migrate
    docker-compose exec web python manage.py createsuperuser

Open http://127.0.0.1:8000/api/docs/.

---

## Environment Variables

All required variables are listed in .env.example:

| Variable        | Description                                       | Example                                          |
|-----------------|---------------------------------------------------|--------------------------------------------------|
| `SECRET_KEY`      | Django secret key (do NOT commit real value)      | `django-insecure-... `                             |
| `DEBUG`           | Debug mode                                        | `True `                                            |`                             |
| `DATABASE_URL`    | PostgreSQL connection URL                         | `postgres://user:pass@localhost:5432/taskflow`     |

For **Docker Compose**, `DATABASE_URL` must use the service name `db`, not `localhost`:

    postgres://taskflow:taskflow@db:5432/taskflow

---

## API Endpoints

### Authentication

| Method | Endpoint                | Description                     |
|--------|-------------------------|---------------------------------|
| POST   | `/api/users/register/`    | Register a new user             |
| POST   |`/api/token/ `            | Obtain access + refresh tokens  |
| POST   | `/api/token/refresh/`     | Refresh an expired access token |
| POST   | `/api/token/verify/`      | Verify a token's validity       |

### Projects

| Method | Endpoint             | Description                    |
|--------|----------------------|--------------------------------|
| GET    | `/api/projects/`       | List your projects             |
| POST   | `/api/projects/ `      | Create a project (owner = you) |
| GET    | `/api/projects/{id}/`  | Retrieve your project          |
| PUT    | `/api/projects/{id}/`  | Full update                    |
| PATCH  | `/api/projects/{id}/`  | Partial update                 |
| DELETE | `/api/projects/{id}/`  | Delete                         |

Query params: `?search=`, `?ordering=created_at|-created_at|name`

### Tasks

| Method | Endpoint          | Description                                              |
|--------|-------------------|----------------------------------------------------------|
| GET    | `/api/tasks/`       | List tasks you can see (owner/assignee)                  |
| POST   | `/api/tasks/`       | Create a task                                            |
| GET    | `/api/tasks/{id}/`  | Retrieve a task                                          |
| PUT    | `/api/tasks/{id}/`  | Full update (owner only)                                 |
| PATCH  | `/api/tasks/{id}/`  | Partial update (owner any field; assignee — only status) |
| DELETE | `/api/tasks/{id}/`  | Delete (owner only)                                      |

Query params: `?status=`, `?priority=`, `?project=`, `?search=`, `?ordering=due_date|-due_date|created_at|priority|status`

### Comments

| Method | Endpoint             | Description                     |
|--------|----------------------|---------------------------------|
| GET    | `/api/comments/`      | List comments you can see       |
| POST   |` /api/comments/`       | Create a comment (author = you) |
| GET    | `/api/comments/{id}/`  | Retrieve a comment              |
| PUT    | `/api/comments/{id}/`  | Full update (author only)       |
| PATCH  | `/api/comments/{id}/`  | Partial update (author only)    |
| DELETE | `/api/comments/{id}/`  | Delete (author only)            |

Query params: `?task=`, `?author=`, `?search=`, `?ordering=created_at|-created_at`

---

## Usage Examples

### 1. Register

```
    curl -X POST http://127.0.0.1:8000/api/users/register/ \
      -H "Content-Type: application/json" \
      -d '{"username": "alice", "email": "alice@example.com", "password": "StrongPass123!", "password2": "StrongPass123!"}'
```

### 2. Obtain JWT tokens

    curl -X POST http://127.0.0.1:8000/api/token/ \
      -H "Content-Type: application/json" \
      -d '{"username": "alice", "password": "StrongPass123!"}'

Response:

    {"access": "eyJhbGciOiJIUzI1NiIs...", "refresh": "eyJhbGciOiJIUzI1NiIs..."}

Save the access token:

    export TOKEN="<paste-access-token-here>"

### 3. Create a project

    curl -X POST http://127.0.0.1:8000/api/projects/ \
      -H "Authorization: Bearer $TOKEN" \
      -H "Content-Type: application/json" \
      -d '{"name": "Website Redesign", "description": "Q1 project"}'

### 4. Create a task

    curl -X POST http://127.0.0.1:8000/api/tasks/ \
      -H "Authorization: Bearer $TOKEN" \
      -H "Content-Type: application/json" \
      -d '{"title": "Draft homepage mockup", "project": 1, "status": "todo", "priority": "high", "due_date": "2026-12-31", "assignees": [1]}'

### 5. Filter + sort + search

    curl -H "Authorization: Bearer $TOKEN" \
      "http://127.0.0.1:8000/api/tasks/?status=todo&priority=high&ordering=due_date&search=mockup"

### 6. Assignee updates status

    curl -X PATCH http://127.0.0.1:8000/api/tasks/1/ \
      -H "Authorization: Bearer $TOKEN" \
      -H "Content-Type: application/json" \
      -d '{"status": "in_progress"}'

### 7. Assignee tries to edit title → 400

    curl -X PATCH http://127.0.0.1:8000/api/tasks/1/ \
      -H "Authorization: Bearer $TOKEN" \
      -H "Content-Type: application/json" \
      -d '{"title": "Hacked"}'

Response:

    400 {"non_field_errors": ["Assignee can only change task status"]}

---

## Data Model

```
    User (AbstractUser)
     |
     |--< Project (owner, PROTECT)
     |    |
     |    |--< Task (project, CASCADE)
     |         |
     |         |--< Comment (task, CASCADE)
     |         |    +-- author -> User (SET_NULL)
     |         |
     |         |--< assignees (M2M) -> User
     |
     |--< comments (author)
```

Key constraints:
- `Project.name` unique per owner (`UniqueConstraint`)
- `Project.owner` — `PROTECT` (cannot delete a user with projects)
- `Task.project` — `CASCADE` (deleting a project removes its tasks)
- `Comment.task` — `CASCADE`
- `Comment.author` — `SET_NULL` (comments survive author deletion, `author=null`)
- `Task.assignees` — `ManyToManyField`, can be empty

---

## Testing

    pytest -v

Covers:
- Model `__str__`, unique constraints, `PROTECT`
- Serializer validation (invalid status, past `due_date`, assignee edit rules)
- API access control (anonymous → 401, foreign project → 404, owner-only edits)

---

## Project Structure

    taskflow/
    |-- config/              # Django project (settings, urls, wsgi/asgi)
    |-- apps/
    |   |-- users/           # custom User model, registration
    |   |-- projects/        # Project model, serializers, views, permissions
    |   |-- tasks/           # Task, Comment, serializers, views, permissions
    |-- Dockerfile
    |-- docker-compose.yml
    |-- pytest.ini
    |-- requirements.txt
    |-- .env.example
    |-- README.md

---

## Known Limitations & Future Work

- `Project.members` — planned M2M for project participants; assignee validation
  against project membership will follow.
- CI — GitHub Actions for `pytest` on every push (planned).
- Swagger screenshot — will be added to the README.
- Frontend — a React/Vue client is out of scope for now.
- Token lifetime — currently 1 hour for `access` (dev convenience); production
  should use 5–15 minutes.

---

## License

MIT — free to use for learning and portfolio purposes.