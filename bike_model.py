from pydantic import BaseModel

class Bike_add(BaseModel):
    name : str
    brand : str
    price : int
    mileage : int
    engine_cc : int
    bike_type : str


class Bike_Update(BaseModel):
    name : str | None = None
    brand : str | None = None
    price : int | None= None
    mileage : int | None = None
    engine_cc : int | None = None
    bike_type : str | None = None