from pydantic import BaseModel

class Car_add(BaseModel):
    name : str
    brand : str
    price : int
    mileage : int
    engine_cc : int
    car_type : str
    
class Car_update(BaseModel):
    name : str | None = None
    brand : str | None = None
    price : int | None= None
    mileage : int | None = None
    engine_cc : int | None = None
    car_type : str | None = None