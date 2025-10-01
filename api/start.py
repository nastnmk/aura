from fastapi import FastAPI
import uvicorn
from api.settings.settings import router as settings_router
from api.user.user_routes import router as user_router
from api.toughts.thoughts_routes import router as thought_router

app = FastAPI()

app.include_router(settings_router)
app.include_router(user_router)
app.include_router(thought_router)

if __name__ == "__main__":
    uvicorn.run("start:app", reload=True)
