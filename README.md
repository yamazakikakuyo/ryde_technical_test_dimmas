# Ryde Interview Backend API

This is a RESTful API built with **FastAPI** and **MongoDB Atlas** to manage user data.  
It was created as part of a technical assessment for Full Stack Engineer (Remote) position.

---

## Features

- Create, Read, Update, Delete (CRUD) users
- Data persisted in MongoDB (Free Tier, Atlas)
- Auto-generated Swagger/OpenAPI docs
- Asynchronous, scalable architecture
- Unit tests with `pytest`
- Secure environment variable management

---

## 🧱 Tech Stack

- **Python 3.11**
- **FastAPI** – Web framework
- **MongoDB Atlas** – Cloud database
- **Motor** – Async MongoDB driver
- **Pydantic** – Data validation
- **Uvicorn** – ASGI server
- **pytest** – Testing framework

---

## 📦 Installation

### 1. Clone the Repository

```
git clone https://github.com/yamazakikakuyo/ryde-api.git
cd ryde-api
````

### 2. Create and Activate Virtual Environment

```
python -m venv ryde_interview_test_dimmas
.\ryde_interview_test_dimmas\Scripts\activate  # Windows
```

### 3. Install Dependencies

```
pip install -r requirements.txt
```

### 4. Configure Environment

Create a `.env` file in the root:

```
MONGO_URI=mongodb+srv://<user>:<pass>@<cluster>.mongodb.net/?retryWrites=true&w=majority
```

---

## 🧪 Running the API

### Start the development server:

```
uvicorn app.main:app --reload
```

* Visit Swagger docs: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
* Visit ReDoc: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

## 🧪 Running Tests

```
pytest
```

Tests are written in `tests/test_users.py` and include:

* Create user
* Read user
* Update user
* Delete user
* Handling Error for every each above activity

---

## 📁 Project Structure

```
app/
├── main.py                 # FastAPI app entry point
├── db/mongo.py             # MongoDB connection
├── models/user.py          # DB logic
├── schemas/user_schema.py  # Pydantic schemas
└── routes/user_routes.py   # API endpoints

tests/
└── test_users.py           # Unit tests
```

---

## ✅ API Endpoints

| Method | Endpoint      | Description       |
| ------ | ------------- | ----------------- |
| POST   | `/users/`     | Create new user   |
| GET    | `/users/`     | List all users    |
| GET    | `/users/{id}` | Get user by ID    |
| PATCH  | `/users/{id}` | Update user by ID |
| DELETE | `/users/{id}` | Delete user by ID |

---

## 💡 Notes

* Uses `python-dotenv` to manage secrets securely.
* MongoDB Free Tier cluster is sufficient for local development.
* Code follows REST and async best practices.

---

## 📬 Contact

If you have any questions, feel free to reach out my email **dimmas3010@gmail.com**.

---
