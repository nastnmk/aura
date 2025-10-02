from fastapi import FastAPI
from models.models import Base
from repositories.settings import engine
from api.user.user_routes import router

app = FastAPI(title="User API")

@app.on_event("startup")
async def on_starting():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        
app.include_router(router)

@app.get("/")
async def root():
    return {"ok": True, "service": "app-api"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
