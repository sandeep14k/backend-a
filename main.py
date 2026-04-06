from fastapi import FastAPI
from database import engine
import models

# Import our modular routers
from routers import users, records, dashboard

# Create DB tables (if they don't exist yet)
models.Base.metadata.create_all(bind=engine)

# Initialize the FastAPI app with metadata
app = FastAPI(
    title="Finance Dashboard API",
    description="An enterprise-grade backend for managing financial records, users, and analytics.",
    version="1.0.0"
)

# Wire up the routers
app.include_router(users.router)
app.include_router(records.router)
app.include_router(dashboard.router)

# A simple health-check route
@app.get("/", tags=["Health"])
def health_check():
    return {"status": "ok", "message": "Finance API is running!"}