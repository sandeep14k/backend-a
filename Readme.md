# Live at - 
https://backend-a-delta.vercel.app

https://backend-a-delta.vercel.app/docs
# Finance Dashboard API

An enterprise-grade backend API built with **FastAPI** and **SQLAlchemy** for managing financial records, user roles, and analytical dashboard data.

## 🏗️ Architecture & Trade-offs

This project was designed with maintainability, separation of concerns, and data safety in mind. While built as an assignment, it follows production-ready patterns:

1. **Domain-Driven Routing:** Routes are split using `APIRouter` (`routers/users.py`, `routers/records.py`, etc.) rather than bloating a single `main.py` file.
2. **Soft Deletes:** Financial records are *never* hard-deleted. Instead, an `is_deleted` flag is flipped in the database. This ensures data integrity and auditability, a standard practice in financial systems.
3. **Advanced SQL Aggregation:** The dashboard summary uses SQLAlchemy's `func.sum` and `group_by` to calculate category-wise totals at the database layer, preventing memory bloat in the Python runtime.
4. **Pagination & Limits:** List endpoints enforce pagination (`skip` and `limit`) with logical boundaries to prevent database crashing or data scraping.
5. **Mock Authentication (Header-based):** To fulfill the assignment's "mock auth" allowance seamlessly, authentication is handled via a custom `user-id` Header Dependency. This cleanly demonstrates Role-Based Access Control (RBAC) and modular FastAPI dependencies without the overhead of setting up a JWT infrastructure for local review.
6. **SQLite Storage:** Chosen to provide a frictionless local evaluation experience without requiring the reviewer to spin up Docker containers or local PostgreSQL databases.

## 📂 Project Structure

```text
finance_backend/
├── database.py       # DB connection and session management
├── models.py         # SQLAlchemy database models (with soft deletes)
├── schemas.py        # Pydantic validation models
├── auth.py           # Authentication and RBAC dependencies
├── routers/          # API Routers for separation of concerns
│   ├── users.py      # User creation and listing
│   ├── records.py    # Financial records with pagination & filtering
│   └── dashboard.py  # Advanced data aggregation logic
├── main.py           # FastAPI application entry point
├── requirements.txt  # Python dependencies
└── README.md         # Project documentation
```

## 🚀 How to Run Locally

**1. Clone the repository and navigate to the project folder:**
```bash
git clone https://github.com/sandeep14k/backend-a.git
cd finance_backend
```
**2. Create and activate a virtual environment:**
# On macOS/Linux
python3 -m venv venv
source venv/bin/activate

# On Windows
python -m venv venv
venv\Scripts\activate

**3. Install dependencies:**

pip install -r requirements.txt

**4. Start the server:**

uvicorn main:app --reload
The API will be available at http://127.0.0.1:8000
