# Simple API ___([0x01.Basic Authentication](https://intranet.alxswe.com/projects/1240))___

Simple HTTP API for playing with `User` model. This folder contains my submissions for the tasks in the project named ___[0x01.BASIC AUTHENTICATION](https://intranet.alxswe.com/projects/1240)___. The project was an introduction to authentication and showed how to implement basic authentication on a simple API. This was simply for academic purposes though, as basic authentication should never be used in a real project.


## Technologies Used
1. Python
2. [Flask](https://palletsprojects.com/p/flask): A simple Python framework for building complex web applications.


## Files

### [models/](models)

- [base.py](models/base.py): base of all models of the API - handle serialization to file
- [user.py](models/user.py): user model

### [api/v1/](api/v1)

- [app.py](api/v1/app.py): entry point of the API
- [auth/auth.py](api/v1/auth/auth.py): template for all authentication systems
- [auth/basic_auth.py](api/v1/auth/basic_auth.py): basic authentication system
- [views/index.py](api/v1/views/index.py): basic endpoints of the API: /status and /stats
- [views/users.py](api/v1/views/users.py): all users endpoints


## Setup

```
$ pip3 install -r requirements.txt
```


## Run
* Without user authentication:
```
$ API_HOST=localhost API_PORT=5000 python3 -m api.v1.app
```

* With basic authentication:
```
$ API_HOST=localhost API_PORT=5000 AUTH_TYPE=basic_auth python3 -m api.v1.app
```


## Routes

- `GET /api/v1/status`: returns the status of the API
- `GET /api/v1/stats`: returns some stats of the API
- `GET /api/v1/users`: returns the list of users
- `GET /api/v1/users/:id`: returns an user based on the ID
- `DELETE /api/v1/users/:id`: deletes an user based on the ID
- `POST /api/v1/users`: creates a new user (JSON parameters: `email`, `password`, `last_name` (optional) and `first_name` (optional))
- `PUT /api/v1/users/:id`: updates an user based on the ID (JSON parameters: `last_name` and `first_name`)
