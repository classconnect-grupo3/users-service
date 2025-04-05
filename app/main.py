from fastapi import FastAPI
from app.config.database.db_init import initialize_database
from app.router.routes import router as api_router

app = FastAPI()

# Initialize the database (create tables if they don't exist)
initialize_database()

# Include the API router
app.include_router(api_router)
