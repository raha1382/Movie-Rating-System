# 🎬 Movie Rating System

A backend REST API project for managing movies, ratings, and analytics, built with **FastAPI**, **PostgreSQL**, **SQLAlchemy**, **Alembic**, **Docker**, and **Poetry**.

---

🌱 Branch Information
This repository uses a structured branching model to separate experimental work, refactoring, and stable releases.

| Branch | Description |
|---------|--------------|
| **`develop/raha`** | 🌱 **Experimental Development Branch** — Includes: Movie creation endpoint , Movie update endpoint , Movie delete endpoint , Filtering functionality for movie listing |
| **`develop/fatemeh`** | 🌱 **Experimental Development Branch** — Includes: List movies endpoint , Movie detail endpoint , Add rating endpoint , Average rating & total ratings count feature |
| **`develop/login`** | 🌱 **Experimental Development Branch using database** — Includes: Structured logging for rating creation , Logging for movie listing endpoint |
| **`main`** | 🧩 **Stable Release Branch** — Complete and stable version of the project. Includes all features.|


---

## 📌 Project Overview

This project is designed to manage:
- Movies and directors
- Movie genres and cast
- User ratings
- Average rating & ratings count per movie
- Filtering and pagination
- Structured logging
- Database seeding from real datasets

---

## 🗂 Tech Stack

- **FastAPI**
- **PostgreSQL**
- **SQLAlchemy**
- **Alembic**
- **Docker & Docker Compose**
- **Poetry**
- **Pydantic**
- **Structured Logging**

---

## 🐳 Docker & Database

This project uses **Docker Compose** to run PostgreSQL.

A `docker-compose.yml` file is included in the project.

---

## 📡 API Examples

### Create Movie
```http
POST /api/v1/movies
```
List Movies (with filters)
```http
GET /api/v1/movies?title=Inception&genre=Action&page=1&page_size=10
```
Get Movie Details
```http
GET /api/v1/movies/{movie_id}
```
Update Movie
```http
PUT /api/v1/movies/{movie_id}
```
Delete Movie
```http
DELETE /api/v1/movies/{movie_id}
```
Add Rating to Movie
```http
POST /api/v1/movies/{movie_id}/ratings
```


---

## 🌱 Database Seeding

### 📁 Seed Data Sources

The seed data is based on the following datasets:

- `tmdb_5000_movies.csv`
- `tmdb_5000_credits.csv`

These files are used to populate movies, directors, cast, and related tables.

---

### ▶ How to Seed the Database

If you want to seed the database, follow these steps:

```bash
docker compose down -v --remove-orphans
docker compose up -d --force-recreate
```
🧱 Run Database Migrations

Apply migrations:
```bash
poetry run alembic upgrade head
```
Create a new migration:
```bash
poetry run alembic revision --autogenerate -m "your_message_here"
```
🔍 Inspect Database Data

To manually inspect database data:
```bash
docker compose exec -it db sh
```
Inside the container:
```bash
psql -U postgres -d movie_db
```
Then you can run this code to see table details:
```bash
\dt
SELECT COUNT(*) FROM movie_ratings;
SELECT * FROM movies LIMIT 5;
```
exit:
```bash
\q
exit
```
---

### 🚀 How to Run the Project

1️⃣ Start Database Container
```bash
docker compose up -d db
```
2️⃣ Install Dependencies
```bash
poetry install
```
3️⃣ Run the Application
```bash
poetry run uvicorn app.main:app --reload
```



The API will be available at:

Swagger UI: http://localhost:8000/docs

ReDoc: http://localhost:8000/redoc
