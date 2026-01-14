from app.api.v1 import router
from app.core.error_handlers import register_error_handlers
from app.db import Base, engine
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Create all database tables (for SQLite dev mode)
Base.metadata.create_all(bind=engine)


def create_app() -> FastAPI:
    app = FastAPI(
        title="CareerPilot API",
        version="1.0.0",
        description="Backend API for the CareerPilot application",
    )

    # CORS for frontend
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Register exception handlers for domain -> HTTP mapping
    register_error_handlers(app)

    app.include_router(router)

    @app.get("/")
    def root():
        return {"message": "Career Pilot backend running"}

    @app.get("/health")
    def health_check():
        return {"status": "ok"}

    return app


# module-level app for uvicorn: `uvicorn app.main:app`
app = create_app()
