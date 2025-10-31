import uvicorn
from application.api.routes.camera_route import camera_router
from fastapi import FastAPI

app = FastAPI()

app.include_router(camera_router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
