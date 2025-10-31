import uvicorn
from fastapi import FastAPI
from routes.dashboard import router_dashboard
from routes.log import router_log
from routes.login import router_login
from routes.user import router_user

app = FastAPI()

app.include_router(router_login)
app.include_router(router_user)
app.include_router(router_log)
app.include_router(router_dashboard)

if __name__ == "__main__":
    uvicorn.run(app, port=8010)
