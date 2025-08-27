from fastapi import FastAPI
from app.routers import logs

app = FastAPI(title="Log Analyzer API")

# "tags" will be used in Swagger documentation to group and describe routes
app.include_router(logs.router, prefix="/logs", tags=["logs"])


@app.get("/")
def index():
    return {"message": "API is running"}
