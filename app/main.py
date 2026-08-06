from fastapi import FastAPI

from app.api.routes.repositories import router as repository_router

app = FastAPI(title="Repo Intelligence API")

app.include_router(repository_router)


@app.get("/health")
def health():
    return {"status": "ok"}
