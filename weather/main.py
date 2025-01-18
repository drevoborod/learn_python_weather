from fastapi import FastAPI, Request

from weather.routers import router


app = FastAPI(title="City temperature retrieval service", docs_url="/")
app.include_router(router)


@app.get("/", summary="Service root and docs URL")
async def root(request: Request):
    return