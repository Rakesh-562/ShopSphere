from fastapi import FastAPI
from app.routes import router
from app.elastic import create_index

app = FastAPI()

@app.on_event("startup")
def startup():
    create_index()

app.include_router(router)