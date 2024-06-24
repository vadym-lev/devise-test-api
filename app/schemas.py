from pydantic import BaseModel
from datetime import datetime

class TestResultBase(BaseModel):
    sensor_type: str
    operator: str
    date: datetime
    success: bool

class TestResultCreate(TestResultBase):
    pass

class TestResult(TestResultBase):
    id: int

    class Config:
        orm_mode: True

class TestResultStatistics(BaseModel):
    sensor_type: str
    total_tests: int
    successful_tests: int
    unsuccessful_tests: int

    class Config:
        orm_mode: True

class ImportResponse(BaseModel):
    message: str