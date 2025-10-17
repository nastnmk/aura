from fastapi import FastAPI
import uvicorn
from aura.api.user.user_routes import router as user_router
from aura.api.settings.settings import router as settings_router
from aura.api.thoughts.stages_routes import router as stage_router
from aura.api.thoughts.thoughts_routes import router as thoughts_router


app = FastAPI(title="User API")

app.include_router(settings_router)
app.include_router(user_router)
app.include_router(thoughts_router)
app.include_router(stage_router)

@app.get("/")
async def root():
    return {"ok": True, "service": "app-api"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
