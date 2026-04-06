# 📊 Finance Dashboard API (Enterprise-Grade Backend)

A highly scalable, production-ready REST API built with **FastAPI** and **SQLAlchemy** for managing financial records, user roles, and analytical dashboard data.

🌍 **Live Base URL:** [https://backend-a-delta.vercel.app](https://backend-a-delta.vercel.app)  
📖 **Interactive API Docs (Swagger UI):** [https://backend-a-delta.vercel.app/docs](https://backend-a-delta.vercel.app/docs)  

---

## 🏗️ Architecture & Engineering Trade-offs

This project was intentionally designed to showcase maintainability, separation of concerns, and data safety. While built as an assignment, it strictly adheres to enterprise-ready patterns:

* **Domain-Driven Routing:** Routes are logically isolated using FastAPI's `APIRouter` (`routers/users.py`, `routers/records.py`, etc.) ensuring the codebase remains clean as it scales.
* **Modern Data Validation:** Fully migrated to **Pydantic V2** (`ConfigDict`) for lightning-fast schema validation and serialization.
* **Data Integrity (Soft Deletes):** Financial records are *never* hard-deleted. An `is_deleted` flag is flipped at the database level. This guarantees auditability, which is a mandatory standard in financial systems.
* **Database-Layer Aggregation:** The dashboard summary relies on SQLAlchemy's `func.sum` and `group_by` to calculate category-wise totals directly inside the database engine, eliminating memory bloat in the Python runtime.
* **Pagination & Rate Protection:** List endpoints enforce pagination boundaries (`skip` and `limit`) to prevent database crashing or malicious data scraping.
* **Serverless Deployment:** Successfully deployed to Vercel utilizing Serverless Functions for high availability and zero-maintenance scaling.

## 🛠️ Tech Stack

* **Framework:** FastAPI (Python)
* **ORM:** SQLAlchemy
* **Database:** SQLite (Chosen for frictionless evaluation and portability)
* **Validation:** Pydantic V2
* **Testing:** Pytest & HTTPX (100% passing automated test suite)
* **Deployment:** Vercel

---

## 🔐 Role-Based Access Control (RBAC)

The system enforces strict RBAC via custom FastAPI dependency injection headers (`user-id`). 

| Role | Capabilities |
| :--- | :--- |
| **Viewer** | Cannot interact with records or dashboard summaries. (Base level logic). |
| **Analyst** | Can read paginated records and access the dashboard aggregation endpoint. Cannot mutate data. |
| **Admin** | Full access. Can create users, create records, soft-delete records, and view summaries. |

---

## 🧪 How to Test the Live API

You do not need to download any code to test this API. You can evaluate the entire system directly through the browser.

1. Navigate to the Live Swagger UI: [https://backend-a-delta.vercel.app/docs](https://backend-a-delta.vercel.app/docs)
2. **Bootstrap the System (Create an Admin):**
   * Open the `POST /users/` endpoint.
   * Click **"Try it out"** and create a user with the role `"admin"`. 
   * Note the `id` returned in the JSON response.
3. **Execute Authenticated Routes:**
   * Open any protected endpoint (e.g., `POST /records/` or `GET /dashboard/summary`).
   * Click **"Try it out"**.
   * You will see a required header field: `user-id`. 
   * Enter your Admin ID to securely authorize the request and bypass the RBAC guard!

---

## 💻 Local Development Setup

If you wish to clone the repository, review the architecture, and run the automated test suite locally, follow these steps:

**1. Clone the repository:**
```bash
git clone https://github.com/sandeep14k/backend-a
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

**4. Run the automated Pytest suite:**

Bash
python -m pytest -v
(The test suite spins up an isolated, in-memory database to verify RBAC security, duplicate-user handling, and core creation logic without affecting local data).

**5. Start the server:**

uvicorn main:app --reload
The API will be available at http://127.0.0.1:8000
