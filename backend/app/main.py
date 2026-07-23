from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database.database import engine, Base
from app.models.models import (
    Employee,
    LoginActivity,
    FileAccess,
    EmailActivity,
    DeviceActivity,
    HttpActivity,
    AnomalyResult,
    User
)

from app.routes import employee
from app.routes import login_activity
from app.routes import file_access
from app.routes import risk
from app.routes import alert
from app.routes import ml
from app.routes import dashboard
from app.routes import anomaly
from app.routes import auth


Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="Insider Threat Behavioral Intelligence System",
    description="AI-powered system to monitor employee behavior, detect insider threats, calculate risk scores, generate alerts, and perform ML-based anomaly detection.",
    version="1.0.0"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(employee.router)
app.include_router(login_activity.router)
app.include_router(file_access.router)
app.include_router(risk.router)
app.include_router(alert.router)
app.include_router(ml.router)
app.include_router(dashboard.router)
app.include_router(anomaly.router)
app.include_router(auth.router)


@app.get("/")
def home():
    return {
        "message": "Welcome to the Insider Threat Behavioral Intelligence System API",
        "version": "2.0.0",
        "status": "Running"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "database": "connected"
    }