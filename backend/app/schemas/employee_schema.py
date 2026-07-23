from pydantic import BaseModel, EmailStr


class EmployeeCreate(BaseModel):
    employee_id: str
    name: str
    department: str
    email: EmailStr


class EmployeeResponse(EmployeeCreate):
    id: int

    class Config:
        from_attributes = True