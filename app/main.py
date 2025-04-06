from fastapi import FastAPI
from app.config.database.db_init import initialize_database
from app.errors.exception_handlers import configure_exception_handlers
from app.router.routes import router as api_router

app = FastAPI()

# Initialize the database (create tables if they don't exist)
initialize_database()

# Include the API router
app.include_router(api_router)

# Register custom exception handlers
configure_exception_handlers(app)
