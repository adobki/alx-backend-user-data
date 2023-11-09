# Simple API ___([0x02.Session Authentication](https://intranet.alxswe.com/projects/1241))___

Simple HTTP API for playing with `User` model. This folder contains my submissions for the tasks in the project named ___[0x02.SESSION AUTHENTICATION](https://intranet.alxswe.com/projects/1241)___. The project was a second introduction to authentication and showed how to manually implement session authentication on a simple API. This was simply for academic purposes though, as session authentication should never be implemented manually in a real project.


## Technologies Used
1. Python
2. [Flask](https://palletsprojects.com/p/flask): A simple Python framework for building complex web applications.


## Files

### [models/](models)

- [base.py](models/base.py): base of all models of the API - handle serialization to file
- [user.py](models/user.py): user model
- [user_session.py](models/user_session.py): session authentication with expiration model

### [api/v1/](api/v1)

- [app.py](api/v1/app.py): entry point of the API


- [auth/auth.py](api/v1/auth/auth.py): template for all authentication systems
- [auth/basic_auth.py](api/v1/auth/basic_auth.py): basic authentication system
- [auth/session_auth.py](api/v1/auth/session_auth.py): session authentication system
- [auth/session_exp_auth.py](api/v1/auth/session_exp_auth.py): session authentication system with session expiration
- [auth/session_db_auth.py](api/v1/auth/session_db_auth.py): session authentication system with session expiration and a database for persistent storage


- [views/index.py](api/v1/views/index.py): basic endpoints of the API: /status and /stats
- [views/users.py](api/v1/views/users.py): all users endpoints
- [views/session_auth.py](api/v1/views/session_auth.py): session authentication endpoints


## Setup

```
$ pip3 install -r requirements.txt
```


## Run
* Without user authentication:
```
$ API_HOST=localhost API_PORT=5000 python3 -m api.v1.app
```

* Basic authentication:
```
$ API_HOST=localhost API_PORT=5000 AUTH_TYPE=basic_auth python3 -m api.v1.app
```

* Session authentication:
```
$ API_HOST=localhost API_PORT=5000 AUTH_TYPE=session_auth SESSION_NAME=_my_session_id python3 -m api.v1.app
```

* Session authentication with session expiration:
```
$ API_HOST=localhost API_PORT=5000 AUTH_TYPE=session_exp_auth SESSION_NAME=_my_session_id SESSION_DURATION=60 python3 -m api.v1.app
```

* Session authentication with session expiration and a database:
```
$ API_HOST=localhost API_PORT=5000 AUTH_TYPE=session_db_auth SESSION_NAME=_my_session_id SESSION_DURATION=60 python3 -m api.v1.app
```


## Routes

- `GET /api/v1/status`: returns the status of the API
- `GET /api/v1/stats`: returns some stats of the API
- `GET /api/v1/users`: returns the list of users
- `GET /api/v1/users/:id`: returns a user based on the ID
- `GET /api/v1/users/me`: returns the user authenticated for the current session 
- `DELETE /api/v1/users/:id`: deletes a user based on the ID
- `POST /api/v1/users`: creates a new user (JSON parameters: `email`, `password`, `last_name` (optional) and `first_name` (optional))
- `PUT /api/v1/users/:id`: updates a user based on the ID (JSON parameters: `last_name` and `first_name`)
- `POST /api/v1/auth_session/login`: used for user login/session creation (Form fields: `email`, `password`)
- `DELETE /api/v1/auth_session/logout`: used for user logout/session deletion (Cookie parameter: `<SERVER_SESSION_NAME>`)
