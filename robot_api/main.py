import uvicorn
from application.api.routes.robot_route import robot_router
from fastapi import FastAPI

app = FastAPI()

app.include_router(robot_router)

if __name__ == "__main__":
    uvicorn.run(app=app)
