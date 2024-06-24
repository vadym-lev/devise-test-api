import csv
import requests
import io
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, models, schemas
from app.database import engine, get_db
from datetime import datetime


app = FastAPI()

models.Base.metadata.create_all(bind=engine)


@app.post("/api_v1/import_csv", response_model=schemas.ImportResponse)
def import_csv(db: Session = Depends(get_db)):
    url = 'https://raw.githubusercontent.com/SukovanchenkoD/ajaxFiles/main/test_results.csv'
    response = requests.get(url)
    response.raise_for_status()  # Ensure we notice bad responses

    file = io.StringIO(response.text)
    reader = csv.DictReader(file)

    for row in reader:
        test_result = schemas.TestResultCreate(
            sensor_type=row['Device type'],
            operator=row['Operator'],
            date=row['Time'],
            success=row['Success'] == '1'
        )
        crud.create_test_result(db=db, test_result=test_result)

    return {"message": "CSV data imported successfully"}


@app.get("/api_v1/stat", response_model=list[schemas.TestResultStatistics])
def get_statistics(
    sensor_type: str = None,
    operator: str = None,
    start_date: datetime = None,
    end_date: datetime = None,
    db: Session = Depends(get_db)
):
    stats = crud.get_statistics(db, sensor_type, operator, start_date, end_date)
    return stats


@app.post("/api_v1/test_result", response_model=schemas.TestResult)
def create_test_result(test_result: schemas.TestResultCreate, db: Session = Depends(get_db)):
    return crud.create_test_result(db=db, test_result=test_result)


@app.delete("/api_v1/test_result/{record_id}", response_model=schemas.TestResult)
def delete_test_result(record_id: int, db: Session = Depends(get_db)):
    db_test_result = crud.delete_test_result(db=db, record_id=record_id)
    if db_test_result is None:
        raise HTTPException(status_code=404, detail="Test result not found")
    return db_test_result