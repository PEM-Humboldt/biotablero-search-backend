from fastapi import FastAPI

from .routers import metrics

app = FastAPI()


app.include_router(metrics.router)


@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}
