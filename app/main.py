from fastapi import FastAPI, Request
from app.routes import user_routes
from app.core.logging_config import logger
from app.db.mongo import init_db_indexes

app = FastAPI(
    title="Ryde Interview API",
    description="RESTful API for managing users.",
    version="1.0.0"
)

@app.on_event("startup")
async def startup_event():
    await init_db_indexes()
    logger.info("MongoDB indexes initialized")

@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"Incoming request: {request.method} {request.url}")
    response = await call_next(request)
    logger.info(f"Response status: {response.status_code}")
    return response

# Register user-related routes under the "/users" prefix
app.include_router(user_routes.router, prefix="/users", tags=["Users"])

# Optional root endpoint
@app.get("/")
def read_root():
    logger.info("Root endpoint called")
    return {"message": "Welcome to the Ryde Interview Test API"}
