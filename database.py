from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# 1. Define the SQLite URL (creates a 'finance.db' file in your root folder)
SQLALCHEMY_DATABASE_URL = "sqlite:///./finance.db"

# 2. Create the SQLAlchemy engine
# 'check_same_thread': False is required to allow FastAPI to handle multiple requests
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# 3. Create a SessionLocal class for database sessions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 4. Create a Base class for your models to inherit from
Base = declarative_base()

# 5. Dependency to get the DB session in your API routes
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()