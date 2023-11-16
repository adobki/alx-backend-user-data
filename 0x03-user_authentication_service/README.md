# ___0x03.User Authentication Service___

This folder contains my submissions for the tasks in the project named ___[0x03.USER AUTHENTICATION SERVICE](https://intranet.alxswe.com/projects/1242)___. The project was a third and final introduction to authentication and showed how to manually implement a user authentication service with SQLAlchemy for database abstraction and a simple Flask API for the interface. This was simply for academic purposes though, as a user authentication service should never be implemented manually in a real project.

## Table of contents
1. [Technologies Used](#Technologies-Used)
2. [Files](#Files)
3. [Setup](#Setup)
4. [Run](#Run)
5. [API Routes](#API-Routes)

## Technologies Used
1. Python
2. [SQLAlchemy](https://www.sqlalchemy.org): A database abstraction library.
3. [Flask](https://palletsprojects.com/p/flask): A simple Python framework for building complex web applications.
4. [Requests](https://requests.readthedocs.io): Python HTTP for Humans.

## Files
- [app.py](app.py): Entry point of the API
- [user.py](user.py): User class model/template for user authentication service
- [db.py](db.py): User authentication model/template with SQLAlchemy for database abstraction
- [auth.py](auth.py): User management and authentication service
- [main.py](main.py): Testcases for user authentication service through the API

## Setup
```
$ pip3 install -r requirements.txt
```

## Run
* Start the user authentication service [API](app.py):
```
./app.py
```
* Run included [testcases](main.py) for the service through the API (while the [API](app.py) is running):
```
./main.py
```

## API Routes
- `GET /`: Returns a welcome message
- `POST /users`: Signup/creates a new user (Form fields: `email`, `password`)
- `POST /sessions`: User login (Form fields: `email`, `password`)
- `DELETE /sessions`: User logout (Cookie: `session_id`)
- `GET /profile`: Returns user profile information (Cookie: `session_id`)
- `POST /reset_password`: Returns password reset token (Form fields: `email`)
- `PUT /reset_password`: Resets a user's password using a reset token (Form fields: `email`, `reset_token`, `new_password`)
