# InterestIntersection - Social Network Web App

A robust, scalable social networking platform built using **Django 5** and **Redis**. Designed for users to connect, share hobbies, bookmark media dynamically, and follow each other's activity streams in real-time.

## 🚀 Key Features

*   **OAuth & Social Authentication**: Integration with external login providers (Google, GitHub, Facebook) using `social-auth-app-django`.
*   **Real-time Activity Stream**: Chronological system that tracks and displays user activities (e.g., following users, bookmarking images) using a highly optimized database schema.
*   **Redis Caching**: Configured Redis database caching layer for fast session storage, improving server response times.
*   **Dynamic Image Bookmarking**: Includes a custom JavaScript **bookmarklet** that allows users to save images from external websites directly onto their profile boards.
*   **Follower System**: Fully implemented follower/following relationships utilizing intermediate join tables to trace connections.
*   **Automated Media Optimization**: Automatic image scaling and responsive thumbnail rendering powered by `easy-thumbnails` and `Pillow`.

---

## 🛠 Tech Stack

- **Backend**: Python, Django 5.x
- **Database**: PostgreSQL (with support for Sqlite in local dev)
- **Cache/Session Manager**: Redis
- **Security**: Python-Decouple (environment variable segregation), Django security middlewares
- **Frontend Utilities**: Django Widget Tweaks (clean form integrations)

---

## 💻 Architecture Details

The system is split into multiple modules:
- `/account`: Handles user signup, login, profile editing, and social authentication configurations.
- `/actions`: Manages the dynamic database structure for user activity tracing.
- `/app`: Root project folder containing middleware, settings, URLs, and static file configurations.

---

## ⚙️ Local Development Guide

### Prerequisites
- Python 3.10+
- Redis Server (local or cloud instance)
- PostgreSQL (optional, defaults to SQLite if database variables are not set)

### 1. Clone & Set Up Directory
```bash
git clone https://github.com/Josue-Tejeda/InterestIntersection.git
cd InterestIntersection
```

### 2. Configure Virtual Environment
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Setup Environment Variables
Create a `.env` file in the root directory:
```env
DEBUG=True
SECRET_KEY=your-django-secret-key
# Redis configuration
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0
```

### 5. Start Redis
Make sure your Redis server is running:
```bash
# On Linux/macOS
redis-server
# On Windows (WSL / native service)
redis-cli ping  # should return PONG
```

### 6. Migrations & Server Launch
```bash
python manage.py migrate
python manage.py runserver
```
Visit `http://127.0.0.1:8000/` in your browser.
