from fastapi import FastAPI
import uvicorn
from api.settings.settings import router as settings_router
from api.user.user_routes import router as user_router
from api.toughts.thoughts_routes import router as thought_router

app = FastAPI(title="User API")

app.include_router(settings_router)
app.include_router(user_router)
app.include_router(thought_router)

@app.get("/")
async def root():
    return {"ok": True, "service": "app-api"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
