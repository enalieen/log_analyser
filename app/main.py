from fastapi import FastAPI
from app.routers import logs
from app.services.elastic import create_index
from app.utils.config import es_client as es


app = FastAPI(title="Log Analyzer API")

# "tags" will be used in Swagger documentation to group and describe routes
app.include_router(logs.router, prefix="/logs", tags=["logs"])


@app.get("/")
def index():
    try:
        es.info()
        r = create_index()
        return {"message": f"API is running. Existing index: {r}"}
    except Exception as e:
        return {"message": f"API is running. Existing index: {e}"}
