# Django Task Manager

A simple task manager built with Django and Vue.js for managing tasks with authentication and filtering features.

## Features
- User authentication (register, login, logout)
- Create, update, delete tasks
- Task filtering (e.g., pending, done)
- Permissions to ensure only task owners can edit or delete tasks
- Token-based authentication using Django Rest Framework (DRF)

## Technologies Used
- Backend: Django, Django REST Framework
- Frontend: Vue.js
- Database: SQLite (default, can be switched to PostgreSQL or MySQL)
- Authentication: Token-based authentication (DRF)
- Styling: Bootstrap (or any CSS framework of your choice)

## Installation
### 1. Clone the Repository
```sh
git clone https://github.com/rohitatzignuts/dj-taskmanager.git
cd django-task-manager
```

### 2. Create and Activate a Virtual Environment
```sh
python -m venv env
source env/bin/activate  # On Windows use: env\Scripts\activate
```

### 3. Install Dependencies
```sh
pip install -r requirements.txt
```

### 4. Apply Migrations & Create Superuser
```sh
python manage.py migrate
python manage.py createsuperuser
```

### 5. Run the Development Server
```sh
python manage.py runserver
```

## API Endpoints
| Method | Endpoint | Description |
|--------|---------|-------------|
| POST | `/register/` | User Registration |
| POST | `/login/` | User Login |
| POST | `/logout/` | User Logout |
| GET | `/tasks/` | Get all tasks |
| POST | `/tasks/` | Create a task |
| GET | `/tasks/{id}/` | Get task details |
| PUT | `/tasks/{id}/` | Update a task |
| DELETE | `/tasks/{id}/` | Delete a task |

## Frontend Setup
Make sure you have **Node.js** installed.
```sh
cd frontend  # Navigate to Vue.js frontend directory
npm install  # Install dependencies
npm run dev  # Start the frontend
```

## Usage
- Register and login to manage tasks.
- Add, update, delete tasks while ensuring only the owner can edit.
- Filter tasks based on their status.
