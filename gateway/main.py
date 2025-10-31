import uvicorn
from application.api.routes.auth_route import auth_router
from application.api.routes.conveyor_belt_route import conveyor_belt_router
from application.api.routes.database_route import database_router
from application.api.routes.user_route import user_router
from fastapi import FastAPI

app = FastAPI()

app.include_router(auth_router)
app.include_router(user_router)
app.include_router(database_router)
app.include_router(conveyor_belt_router)

if __name__ == "__main__":
    uvicorn.run(app=app, port=8010)
