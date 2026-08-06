CRM System

A scalable and secure Customer Relationship Management (CRM) platform. The backend is built with Django and Django REST
Framework, providing a robust API, while the frontend is a modern web application running independently. The entire
infrastructure is containerized using Docker for seamless deployment.

---

Tech Stack

| Layer            | Technology                                    |
|:-----------------|:----------------------------------------------|
| Backend          | Django, Django REST Framework                 |
| Frontend         | Modern JS Framework (Accessible on Port 3000) |
| Database         | MySQL                                         |
| Containerization | Docker, Docker Compose                        |

---

Environment Setup

Create a `.env` file in the **root** of the project (next to `docker-compose.yml`) similar to `.env.example`.

> **Important:** You must open the `.env` file and fill in your actual data before running the project. The
> application will not start without the following configured:
> * `SECRET_KEY` (Django secret key)
> * Database credentials 


Running the Project

### 1. Clone the repository

### 2. Create the `.env` file

Copy the template and fill in your values.

### 3. Build and start containers
```bash
docker compose up --build
```
*(Note: To run the containers in the background, append `-d` to the command: `docker compose up --build -d`)*

This command will:
- Build the backend and frontend Docker images.
- Start the database container (if included in your compose file).
- Start the Django REST Framework API server.
- Start the Frontend server.
