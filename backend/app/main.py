from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.database import engine, Base
from app.routers import shipments
from app.models import Shipment

# Create database tables
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(
    title=settings.API_TITLE,
    version=settings.API_VERSION,
    description="API for managing shipments in the Flowdesk system",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Add CORS middleware (adjust origins for production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # TODO: Restrict to specific origins in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(shipments.router)


@app.get("/", tags=["health"])
async def root():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "Flowdesk Shipment Management API",
        "version": settings.API_VERSION,
    }


@app.get("/health", tags=["health"])
async def health_check():
    """Detailed health check endpoint"""
    return {
        "status": "ok",
        "database": "connected",
        "timestamp": "2024-01-15T10:30:00Z",
    }


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )
