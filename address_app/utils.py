from sqlalchemy.orm import Session
from geopy.distance import geodesic
from . import models, schemas

# Function to retrieve an address by its ID


def get_address(db: Session, address_id: int):
    return db.query(models.Address).filter(models.Address.id == address_id).first()

# Function to create a new address


def create_address(db: Session, address: schemas.AddressCreate):
    db_address = models.Address(
        address=address.address,
        latitude=address.latitude,
        longitude=address.longitude
    )
    db.add(db_address)
    db.commit()
    db.refresh(db_address)
    return db_address

# Function to retrieve an address by its coordinates


def get_address_by_coordinates(db: Session, latitude: str, longitude: str):
    return db.query(models.Address).filter(
        models.Address.latitude == latitude,
        models.Address.longitude == longitude
    ).first()

# Function to retrieve all addresses


def get_all_addresses(db: Session):
    return db.query(models.Address).all()

# Function to update an address


def update_address(db: Session, address_id: int, address: schemas.AddressUpdate):
    db_address = db.query(models.Address).get(address_id)
    if db_address:
        # Update only the fields that are provided in the request body
        for key, value in address.dict(exclude_unset=True).items():
            setattr(db_address, key, value)
        db.commit()
        db.refresh(db_address)
    return db_address

# Function to delete an address


def delete_address(db: Session, address_id: int):
    db_address = db.query(models.Address).get(address_id)
    if db_address:
        db.delete(db_address)
        db.commit()
    return db_address

# Function to find nearby addresses within a given distance from a specified location


def find_nearby_addresses(db, latitude, longitude, distance):
    addresses = get_all_addresses(db)
    nearby_addresses = []

    origin_point = (latitude, longitude)

    # Using geodesic module for calculating the distance between two coordinates
    for address in addresses:
        address_point = (address.latitude, address.longitude)
        dist_km = geodesic(origin_point, address_point).kilometers
        if dist_km <= distance:
            nearby_addresses.append({
                "id": address.id,
                "address": address.address,
                "latitude": address.latitude,
                "longitude": address.longitude
            })
    return nearby_addresses
