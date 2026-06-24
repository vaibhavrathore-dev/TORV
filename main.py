from fastapi import FastAPI
from app.routes.car_routes import car_router
from app.routes.bike_routes import router
from app.routes.auth_routes import auth_router
from app.database import client
app = FastAPI()
@app.get("/")
def home():
    client.admin.command("ping")
    return {"message": "MongoDB Connected Successfully"}

app.include_router(router)
app.include_router(car_router)
app.include_router(auth_router)