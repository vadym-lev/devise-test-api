from sqlalchemy import Column, Integer, String, Boolean, DateTime
from app.database import Base


class TestResult(Base):
    __tablename__ = "test_results"

    id = Column(Integer, primary_key=True, index=True)
    sensor_type = Column(String, index=True)
    operator = Column(String, index=True)
    date = Column(DateTime)
    success = Column(Boolean)

