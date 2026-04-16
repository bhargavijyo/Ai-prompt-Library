# AI Prompt Library Management System

A full-stack application built for managing and exploring AI image generation prompts. Features a high-performance Redis-backed view counter, tag-based categorization, and a premium modern UI.

## 🚀 Tech Stack

- **Frontend:** Angular 21 (Standalone Components)
- **Backend:** Python / Django (Pure native views)
- **Database:** PostgreSQL
- **Cache:** Redis (Source of truth for view counts)
- **Containerization:** Docker & Docker Compose

## ✨ Key Features

- **Prompt Management:** Create, view, and organize prompts with complexity levels.
- **Real-time View Counter:** Leveraging Redis for atomic increments on prompt views.
- **Tagging System:** Categorize prompts with custom tags (e.g., cyberpunk, anime).
- **Premium UI:** Dark-mode "Glassmorphism" interface with smooth transitions and HSL color palettes.
- **Reactive Forms:** Robust client-side validation for a seamless user experience.
- **CORS Enabled:** Secure communication between decoupled frontend and backend.

## 🛠 Setup & Running

The entire stack is containerized for ease of use.

### Prerequisites
- Docker & Docker Compose

### Run with one command:
```bash
docker-compose up --build
```

The application will be available at:
- **Frontend:** [http://localhost:4200](http://localhost:4200)
- **Backend API:** [http://localhost:8000/prompts/](http://localhost:8000/prompts/)
- **Admin Panel:** [http://localhost:8000/admin/](http://localhost:8000/admin/)

### 🔑 Create Admin User (Optional)
To access the Django Admin, run:
```bash
docker-compose exec backend python manage.py createsuperuser
```

### 🌱 Seed Sample Data
To populate the library with a beautiful initial dataset:
```bash
docker-compose exec backend python seed_data.py
```
This will create 5 premium prompts with tags and an admin user (`admin` / `admin123`).


## 📐 Architectural Decisions

- **Redis View Counter:** Chosen to offload frequent "view" writes from the primary relational database, ensuring high performance even under heavy traffic. Redis remains the source of truth for these counts.
- **Standalone Components:** Used the latest Angular patterns (v21) to minimize boilerplate and improve application performance.
- **Native Django Views:** Avoided DRF as per requirement, implementing a lightweight JSON-based API using `JsonResponse` and standard Django models.
- **Dynamic Proxy:** Configured Angular dev server with a proxy to avoid CORS issues during development and provide a cleaner URL structure (`/api/*`).

## 📁 Project Structure

```text
ai-prompt-library/
├── backend/            # Django Application
│   ├── config/         # Project settings
│   ├── prompts/        # Core logic & Models
│   └── Dockerfile
├── frontend/           # Angular Application
│   ├── src/app/        # Components & Services
│   └── Dockerfile
└── docker-compose.yml  # Orchestration
```
