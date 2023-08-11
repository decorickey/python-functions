import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum

from .bmonster import api as bmonster


if os.environ["STAGE"] == "local":
    app = FastAPI(docs_url="/api/docs/")
    app.add_middleware(
        CORSMiddleware, allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"]
    )
else:
    app = FastAPI()

app.include_router(bmonster.router, prefix="/api/bmonster")
handler = Mangum(app)


@app.get("/api/ping/")
async def ping():
    return "ping"
