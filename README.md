# Ryde Interview Backend API

This is a RESTful API built with **FastAPI** and **MongoDB Atlas** to manage user data.  
It was created as part of a technical assessment for Full Stack Engineer (Remote) position.

---

## Features

- Create, Read, Update, Delete (CRUD) users
- Following and Follower system with nearby friend feature
- Data persisted in MongoDB (Free Tier, Atlas)
- Auto-generated Swagger/OpenAPI docs
- Asynchronous, scalable architecture
- Unit tests with `pytest`
- Secure environment variable management
- Logging system that written in console and file

---

## Tech Stack

- **Python 3.11** - Programming Environment
- **MongoDB Atlas** – Cloud database
- **FastAPI** – Web framework (0.115.13)
- **Motor** – Async MongoDB driver (3.7.1)
- **Pydantic** – Data validation (2.11.7)
- **Uvicorn** – ASGI server (0.34.3)
- **pytest** – Testing framework (8.4.1)

---

## Project Structure

```
app/
├── main.py                 # FastAPI app entry point
├── core/
    ├── loggin_config.py    # Logging configuration
├── db/
    ├── mongo.py            # MongoDB connection
├── models
    ├── user.py             # DB (MongoDB) connection, index, and other configuration
├── schemas
    ├── user_schema.py      # Pydantic schemas
└── routes
    ├── user_routes.py      # API endpoints

tests/
└── test_users.py           # Unit tests

logs/
└── app.log                 # Logging Output. Automatically created when running REST API server.
```

---

## Installation

### 1. Clone the Repository

```
git clone https://github.com/yamazakikakuyo/ryde_technical_test_dimmas.git
cd ryde_technical_test_dimmas
```

### 2. Create and Activate Virtual Environment

```
python -m venv ryde_interview_test
.\ryde_interview_test\Scripts\activate  # Windows
```

### 3. Install Dependencies

```
pip install -r requirements.txt
```

### 4. Configure Environment

Create a `.env` file in the root, then, add line below. Adjust <user>, <pass>, and <cluster> with your own Connection String for MongoDB

```
MONGO_URI=mongodb+srv://<user>:<pass>@<cluster>.mongodb.net/?retryWrites=true&w=majority
```

---

## Running the API

### Start the server:
Remove the `--reload` if running server in production mode
```
uvicorn app.main:app --reload
```

* Visit Swagger docs: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
* Visit ReDoc: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

## Running Tests
To run test case, just use command below:
```
pytest
```

All test scripts are written in `tests/*.py` and include test case like below:

1. test_users_crud_basic.py
    * Test Create, Read, Update, Delete user
    * Test Handling Error duplicate username upon creation or change user
    * Test Handling Error for not complete data upon creation user
    * Test Handling Error wrong date format
    * and other tests ...
2. test_users_follow_system.py
    * Test Follow, Unfollow, Get Follower, and Get Following
    * Test Handling Error same person follow
    * Test Handling Error non-exist user in follow (as follower or target)
    * and other tests ...
3. test_users_nearby_system.py
    * Test Nearby Following Friends System
    * Test Handling Error non-exist user
    * Cross check friend list based on within distance nearby range or not
    * and other tests ...

---

## API Endpoints

| Method | Endpoint                                | Description                                                                |
| ------ | --------------------------------------- | -------------------------------------------------------------------------- |
| POST   | `/users/`                               | Create new user                                                            |
| GET    | `/users/`                               | List all users                                                             |
| GET    | `/users/{id}`                           | Get user by ID                                                             |
| PATCH  | `/users/{id}`                           | Update user by ID                                                          |
| DELETE | `/users/{id}`                           | Delete user by ID                                                          |
| PATCH  | `/users/{user_id}/follow/{target_id}`   | User by ID user_id follows user with ID target_id                          |
| PATCH  | `/users/{user_id}/unfollow/{target_id}` | User by ID user_id unfollows user with ID target_id                        |
| GET    | `/users/{user_id}/followers`            | Follower list of user                                                      |
| GET    | `/users/{user_id}/following`            | Following list of user                                                     |
| GET    | `/users/{username}/nearby-friends`      | Nearby friend from user following list for certain distance using username |

---

## Notes

* Uses `python-dotenv` to manage secrets securely.
* MongoDB Free Tier cluster is sufficient for local development.
* Code follows REST and async best practices.

---

## Contact

If you have any questions, feel free to reach out my email **dimmas3010@gmail.com**.

---
