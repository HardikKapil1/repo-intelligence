from fastapi import FastAPI

app = FastAPI(title="Repo Intelligence API")


@app.get("/health")
def health():
    return {"status": "ok"}
