# Snip — Long URLs Made Short

A full-stack URL shortening service inspired by Bitly. Users paste a long URL, receive a shortened link, and are seamlessly redirected when that link is visited. The project emphasizes a robust, production-aware backend built with Django and supporting infrastructure.

---

## Tech Stack

### Backend *(primary focus)*
| Technology | Role |
|---|---|
| **Django** | Web framework |
| **Django REST Framework** | API layer |
| **PostgreSQL** | Persistent storage for URL mappings |
| **Celery** | Asynchronous task scheduling (garbage collection) |
| **Redis** | Celery message broker / task queue |
| **Docker** | Containerised Redis instance |

### Frontend *(scaffolded separately)*
| Technology | Role |
|---|---|
| SvelteKit | UI framework |
| Bun | JavaScript runtime & package manager |
| Vite | Build tool & dev server |

---

## How It Works

1. A user visits the Snip frontend and pastes a long URL into the input field.
2. They click **Shorten** — the frontend sends a `POST` request to the Django REST API.
3. The backend generates a **random alphanumeric code**, stores the `code → original URL` mapping in PostgreSQL, and returns the full shortened URL to the client.
4. The user can **copy** the shortened link or **click it directly** in the UI.
5. Clicking the shortened link hits the frontend domain, which calls the backend with the code. The backend looks up the code in the database and **redirects** the user to the original URL.

---

## Backend Architecture

### URL Shortening Endpoint
- Accepts a long URL via `POST` request
- Generates a unique random alphanumeric slug
- Persists the `slug → URL` mapping to PostgreSQL
- Returns the complete shortened URL

### Redirect Endpoint
- Accepts a slug via `GET` request
- Queries PostgreSQL for the matching original URL
- Issues an HTTP redirect to the resolved destination

### Garbage Collection (Celery + Redis)
One of the more architecturally interesting aspects of this project is automated link expiry. Rather than allowing the database to grow indefinitely, the backend runs a **scheduled Celery task** that:

- Identifies any links that have not been accessed within the last **5 minutes**
- Deletes those records from PostgreSQL automatically
- Runs continuously in the background, brokered through **Redis**

This keeps the database lean without any manual intervention, and demonstrates practical use of distributed task scheduling in a Django environment.

---

## Key Backend Concepts Demonstrated

- **RESTful API design** with Django REST Framework
- **Relational database modelling** with PostgreSQL
- **Asynchronous task processing** with Celery
- **Message brokering** with Redis
- **Scheduled background jobs** for automated data lifecycle management
- **Stateless redirect logic** via slug-based database lookups
- **Containerisation** with Docker for running the Redis instance
