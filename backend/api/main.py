from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from db.setup import setup_database
from db.parser import parser
from api.routes import router as api_router
import api.routes as routes_module
from api.websocket import router as ws_router
import api.websocket as ws_module

app = FastAPI()

# Enable CORS for Vite (port 5173)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# 1. Initialize Engine
db, executor = setup_database()


routes_module.db = db
routes_module.executor = executor
routes_module.parser = parser

ws_module.db = db

app.include_router(api_router)
app.include_router(ws_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)