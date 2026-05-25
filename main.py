from fastapi import FastAPI
from app.backend.database import engine, Base
import app.backend.model
app = FastAPI()
# 테이블 생성
Base.metadata.create_all(bind=engine)

@app.get("/")
def root():
    return {"message": "Hello World"}