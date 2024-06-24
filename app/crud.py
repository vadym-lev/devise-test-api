from sqlalchemy.sql import func, case
from sqlalchemy.orm import Session
from datetime import datetime
from app import models, schemas


def get_statistics(
        db: Session,
        sensor_type: str = None,
        operator: str = None,
        start_date: datetime = None,
        end_date: datetime = None
):
    query = db.query(
        models.TestResult.sensor_type,
        func.count(models.TestResult.id).label('total_tests'),
        func.sum(case((models.TestResult.success == 1, 1), else_=0)).label('successful_tests'),
        func.sum(case((models.TestResult.success == 0, 1), else_=0)).label('unsuccessful_tests')
    ).group_by(models.TestResult.sensor_type)

    if sensor_type:
        query = query.filter(models.TestResult.sensor_type == sensor_type)

    if operator:
        query = query.filter(models.TestResult.operator == operator)

    if start_date:
        query = query.filter(models.TestResult.date >= start_date)

    if end_date:
        query = query.filter(models.TestResult.date <= end_date)

    return query.all()


def create_test_result(db: Session, test_result: schemas.TestResultCreate):
    db_test_result = models.TestResult(**test_result.dict())
    db.add(db_test_result)
    db.commit()
    db.refresh(db_test_result)
    return db_test_result


def delete_test_result(db: Session, record_id: int):
    db_test_result = db.query(models.TestResult).filter(models.TestResult.id == record_id).first()
    if db_test_result is None:
        return None
    db.delete(db_test_result)
    db.commit()
    return db_test_result

