from fastapi import APIRouter
from bson import ObjectId
from app.database import cars_collection
from app.models.car_model import Car_add,Car_update
from fastapi import Depends
from app.services.auth_service import get_current_user, admin_required


car_router = APIRouter()
@car_router.get("/cars" ,  current_user = Depends(get_current_user))
def get_cars():
    cars = list(cars_collection.find())
    for car in cars:
        car["_id"] = str(car["_id"])
    return cars

@car_router.get("/cars/search" ,  current_user = Depends(get_current_user))
def search_car(name : str):
    cars = list(cars_collection.find({"name" : {"$regex" : name , "$options" : "i"}}))
    for car in cars:
     car["_id"] =  str(car["_id"])
    return car

@car_router.get("/cars/filter" ,  current_user = Depends(get_current_user))
def filter_cars(brand : str | None = None,
                price : int | None = None,
                mileage : int | None = None,
                engine_cc : int | None = None,
                car_type : str | None = None):
    filter_query = {}
    if brand:
        filter_query["brand"] = {"$regex" : brand ,"$options" :"i"}
    if mileage:
        filter_query["mileage"] = {"$gte" : mileage}
    if price:
        filter_query["price"] = {"$lte" : price}
    if engine_cc:
        filter_query["engine_cc"] = {"$lte" : engine_cc}
    if car_type:
        filter_query["car_type"] = {"$regex" : car_type , "$options" : "i"}
    
    cars = list(cars_collection.find(filter_query))
    for car in cars:
        car["_id"] = str(car["_id"])
    return cars

@car_router.get("/cars/sort" ,  current_user = Depends(get_current_user))
def sort_cars(field : str = "price" , order : str = "asc"):
    allowed_fields = ["price" , "mileage" , "engine_cc"]
    allowed_orders = ["asc" , "desc"]
    if field not in allowed_fields:
        return {
            "message" : "Invalid field for sorting"
        }
    if order not in allowed_orders:
        return {
            "message" : "Invalid order for sorting"
        }
    if order == "asc":
        sort_order = 1
    else:
        sort_order = -1

    cars = list(cars_collection.find().sort(field , sort_order))
    for car in cars:
        car["_id"] = str(car["_id"])
    return cars

car_router.get("/cars/{car_id}" ,  current_user = Depends(get_current_user))
def get_car_id(car_id : str):
    car = cars_collection.find_one({"_id" : ObjectId(car_id)})
    car["_id"] = str(car["_id"])
    return car



@car_router.post("/cars" , current_user = Depends(admin_required))
def add_car(car : Car_add):
    new_car = car.model_dump()
    result = cars_collection.insert_one(new_car)
    return {
        "message" : "Car Added Successfully",
        "id" : str(result.inserted_id)
    }
    
@car_router.delete("/cars/{car_id}" ,  current_user = Depends(admin_required))
def remove_bike(car_id : str):
    result = cars_collection.delete_one({"_id" : ObjectId(car_id)})
    if result.deleted_count == 0:
        return {
            "message" : "Car deleted succesfully"
        }
    else:
        return {
            "message" : "Car not found"
        }
    
@car_router.patch("/cars/{car_id}" ,  current_user = Depends(admin_required))
def update_car(car : Car_update,car_id : str):
    updated_car = car.model_dump(exclude_unset=True)
    result = cars_collection.update_one({"_id" : ObjectId(car_id)} , {"$set" : updated_car})
    if result.matched_count != 0 and result.modified_count == 0:
        return {
            "message" : "Car was Found but cannot be updated because you are providing existing data"
        }
    if result.matched_count != 0 and result.modified_count != 0:
        return{
            "message" : "Car was Updated Successfully"
        }
    if result.matched_count == 0 :
        return {
            "message" : " Car was Not Found so it cannot be updated"
        }