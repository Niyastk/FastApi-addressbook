from pydantic import BaseModel, Field, field_validator, validator
from typing import Optional


class AddressBase(BaseModel):
    """
    Base model for an address.

    Attributes:
        address (str): Name of the city or place.
        latitude (float): Latitude of the origin point.
        longitude (float): Longitude of the origin point.
    """

    address: str = Field(..., description="Name of the city or place")
    latitude: float = Field(..., description="Latitude of the origin point")
    longitude: float = Field(..., description="Longitude of the origin point")

    @field_validator("latitude")
    def validate_latitude(cls, v):
        if v < -90 or v > 90:
            raise ValueError("Latitude must be between -90 and 90 degrees")
        return v

    @field_validator("longitude")
    def validate_longitude(cls, v):
        if v < -180 or v > 180:
            raise ValueError("Longitude must be between -180 and 180 degrees")
        return v


class AddressCreate(AddressBase):
    """
    Schema for creating a new address.
    Inherits from AddressBase.
    """

    pass


class Address(AddressBase):
    """
    Schema for retrieving an address including the ID.
    Inherits from AddressBase.

    Attributes:
        id (int): Identifier for the address.
    """

    id: int


class AddressUpdate(BaseModel):
    """
    Schema for updating an address.

    Attributes:
        address (str, optional): Optional field to update the address.
        latitude (float, optional): Optional field to update the latitude.
        longitude (float, optional): Optional field to update the longitude.
    """

    address: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None

    @field_validator("latitude", "longitude")
    def validate_lat_lon(cls, v):
        if v is not None and (v < -90 or v > 90 if "latitude" else v < -180 or v > 180):
            raise ValueError(
                f"Invalid {'latitude' if 'latitude' else 'longitude'} value"
            )
        return v
