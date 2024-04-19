from pydantic import BaseModel, Field
from typing import Optional

# Base model for Address
class AddressBase(BaseModel):
    address: str = Field(..., description="Name of the city or place")
    latitude: float = Field(..., description="Latitude of the origin point")
    longitude: float = Field(..., description="Longitude of the origin point")

# Schema for creating a new Address
class AddressCreate(AddressBase):
    pass

# Schema for retrieving an Address
class Address(AddressBase):
    id: int

# Schema for updating an Address
class AddressUpdate(BaseModel):
    address: Optional[str] = None  # Optional field to update the address
    latitude: Optional[float] = None  # Optional field to update the latitude
    longitude: Optional[float] = None  # Optional field to update the longitude