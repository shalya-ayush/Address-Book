# Address Book API
A simple Address Book REST API built with FastAPI, SQLAlchemy, and SQLite.

This API allows users to:

- Create addresses
- Update addresses
- Delete addresses
- Retrieve addresses
- Find nearby addresses within a given distance

## 🛠️ Tech Stack

- FastAPI
- SQLAlchemy
- SQLite
- Pydantic
- Uvicorn


## ⚙️ Setup Instructions

### 1. Clone the Repository

```
git clone https://github.com/shalya-ayush/Address-Book.git
cd address_book
```
### 2. Create Virtual Environment

Windows:

```
python -m venv venv
venv\Scripts\activate
```

Mac/Linux:

```
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```
pip install -r requirements.txt
```

### 4. Run the Application

Make sure you are in the project root directory.

```
uvicorn app.main:app --reload
```
### 5. Access the API

```
http://127.0.0.1:8000/
```

## 👨‍💻Author

Ayush Shalya