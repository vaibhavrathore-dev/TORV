from fastapi import APIRouter
from bson import ObjectId
from app.database import bikes_collection
from app.models.bike_model import Bike_add,Bike_Update
from fastapi import Depends
from app.services.auth_service import get_current_user, admin_required

router = APIRouter()

@router.get("/bikes")
def get_bikes(current_user = Depends(get_current_user)):
    bikes = list(bikes_collection.find())
    for bike in bikes:
        bike["_id"] = str(bike["_id"])
    return bikes

@router.get("/bikes/search")
def search_bike(name : str , current_user = Depends(get_current_user)):
    bikes = list(bikes_collection.find({"name" : {"$regex" : name , "$options" : "i"}}))
    for bike in bikes:
     bike["_id"] =  str(bike["_id"])
    return bikes

@router.get("/bikes/filter" , current_user = Depends(get_current_user))
def filter_bikes(brand : str | None=None,
                 price : int | None = None,
                 mileage : int| None = None,
                 engine_cc : int| None = None,
                 bike_type : str | None = None):
    filter_query = {}
    if brand:
        filter_query["brand"] = {"$regex" : brand,"$options" : "i"}
    if price:
        filter_query["price"] = {"$lte" : price}
    if mileage:
        filter_query["mileage"] = {"$gte" : mileage}
    if engine_cc:
        filter_query["engine_cc"] =  {"$lte" : engine_cc}
    if bike_type:
        filter_query["bike_type"] = {"$regex" : bike_type , "$options" : "i"}

    bikes = list(bikes_collection.find(filter_query))
    for bike in bikes:
        bike["_id"] = str(bike["_id"])
    return bikes      


@router.get("/bikes/sort" , current_user = Depends(get_current_user))
def sort_bikes(field :str = "price" , order : str = "asc"):
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
    bikes = list(bikes_collection.find().sort(field,sort_order))
    for bike in bikes:
        bike["_id"] = str(bike["_id"])
    return bikes        

@router.get("/bikes/{bike_id}" , current_user = Depends(get_current_user)) 
def get_bike_id(bike_id : str):
    bike = bikes_collection.find_one({"_id" : ObjectId(bike_id)})
    bike["_id"] = str(bike["_id"])
    return bike

@router.delete("/bikes/{bike_id}" , current_user = Depends(admin_required))
def remove_bike(bike_id : str):
    result = bikes_collection.delete_one({"_id" : ObjectId(bike_id)})
    if result.deleted_count != 0:
        return {
            "message" : "Bike deleted succesfully"
        }
    else:
        return {
            "message" : "Bike not found"
        }
@router.post("/bikes" , current_user = Depends(admin_required))
def add_bike(bike : Bike_add):
    new_bike = bike.model_dump()
    result = bikes_collection.insert_one(new_bike)
    return {
        "message" : "Bike Added Successfully",
        "id" : str(result.inserted_id)
    }
    
@router.patch("/bikes/{bike_id}" , current_user = Depends(admin_required))
def update_bike(bike : Bike_Update,bike_id : str):
    updated_bike = bike.model_dump(exclude_unset=True)
    result = bikes_collection.update_one({"_id" : ObjectId(bike_id)} , {"$set" : updated_bike})
    if result.matched_count != 0 and result.modified_count == 0:
        return {
            "message" : "Bike was Found but cannot be updated because you are providing existing data"
        }
    if result.matched_count != 0 and result.modified_count != 0:
        return{
            "message" : "Bike was Updated Successfully"
        }
    if result.matched_count == 0 :
        return {
            "message" : " Bike was Not Found so it cannot be updated"
        }