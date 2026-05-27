# config.py


from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
app = FastAPI()
origins = [
    "http://localhost:5173", # Vite
    "http://127.0.0.1:5173",
    "http://localhost:5500", # Live Server (Add this!)
    "http://127.0.0.1:5500",
]
app.add_middleware( 
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)