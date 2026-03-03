from pydantic import BaseModel, Field

class AddressBase(BaseModel):
    name: str      = Field(..., min_length=1, max_length=100, example="Home")
    street: str    = Field(..., min_length=1, max_length=200, example="123 MG Road")
    city: str      = Field(..., min_length=1, max_length=100, example="Mumbai")
    country: str   = Field(..., min_length=1, max_length=100, example="India")
    latitude: float  = Field(..., ge=-90,  le=90,  example=19.0760)
    longitude: float = Field(..., ge=-180, le=180, example=72.8777)


class AddressCreate(AddressBase):
    pass

class AddressUpdate(AddressBase):
    pass

class AddressResponse(AddressBase):
    id: int

    class Config:
        from_attributes = True