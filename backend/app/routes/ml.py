from fastapi import APIRouter
from pydantic import BaseModel

from app.services.ml_engine import predict_risk

router = APIRouter(
    prefix="/ml",
    tags=["Machine Learning"]
)


class EmployeeFeatures(BaseModel):
    failed_logins: int
    file_reads: int
    file_writes: int
    file_deletes: int


@router.post("/predict")
def predict(employee: EmployeeFeatures):

    features = [
        employee.failed_logins,
        employee.file_reads,
        employee.file_writes,
        employee.file_deletes
    ]

    return predict_risk(features)