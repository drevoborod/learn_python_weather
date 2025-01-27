from fastapi import FastAPI

from weather.routers import router


app = FastAPI(title="City temperature retrieval service", docs_url="/")
app.include_router(router)
