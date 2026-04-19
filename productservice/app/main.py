from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import router
from app.elastic import create_index

app = FastAPI()
app.add_middleware(CORSMiddleware,allow_origins=["*"],allow_credentials=True,allow_methods=["*"],allow_headers=["*"],)

@app.on_event("startup")
def startup():
    try:
        create_index()
    except Exception as e:
        print (f" Elastic search is not running {e}")


app.include_router(router)