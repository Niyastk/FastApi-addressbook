from fastapi import APIRouter

from fastapi import HTTPException, Depends, Query
from fastapi.responses import JSONResponse
from address_app import utils, schemas, models
from address_app.models import Base

from sqlalchemy.orm import Session


from db.database import SessionLocal

router = APIRouter(tags=["Address Crud operations"])


# Function to retrieve a database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# create new address
@router.post("/addresses/", response_model=schemas.Address, status_code=201)
def create_address(address: schemas.AddressCreate, db: Session = Depends(get_db)):
    db_address = utils.get_address_by_coordinates(
        db=db, latitude=address.latitude, longitude=address.longitude)
    if db_address:
        raise HTTPException(status_code=400, detail="Address already exists.")
    return utils.create_address(db, address=address)


# get all the addresses
@router.get('/addresses_all/', response_model=list[schemas.Address])
def list_addresses(db: Session = Depends(get_db)):
    addresses = utils.get_all_addresses(db)
    if len(addresses) == 0:
        raise HTTPException(
            status_code=404, detail="No address found in database.")
    return addresses


# get a single address
@router.get('/addresses/{address_id}', response_model=schemas.Address)
def get_address_by_id(address_id: int, db: Session = Depends(get_db)):
    address = utils.get_address(db=db, address_id=address_id)
    if address is None:
        raise HTTPException(status_code=404, detail="Address not found.")
    return address


# Update an address
@router.put("/addresses/{address_id}", response_model=schemas.Address)
def update_address(address_id: int, address: schemas.AddressUpdate, db: Session = Depends(get_db)):
    db_address = utils.get_address(db=db, address_id=address_id)
    if db_address is None:
        raise HTTPException(status_code=404, detail="Address not found.")
    return utils.update_address(db=db, address_id=address_id, address=address)


# Delete an address
@router.delete("/addresses/{address_id}", response_model=schemas.Address)
def delete_address(address_id: int, db: Session = Depends(get_db)):
    db_address = utils.get_address(db=db, address_id=address_id)
    if db_address is None:
        raise HTTPException(status_code=404, detail="Address not found.")
    return utils.delete_address(db=db, address_id=address_id)


# get near by addresses
@router.get("/nearby_adresses", response_model=schemas.Address, tags=['Nearby Address'])
def get_nearby_addresses(
    latitude: float = Query(..., description="Latitude of the origin point"),
    longitude: float = Query(..., description="Longitude of the origin point"),
    distance: float = Query(...,
                            description="Maximum distance in kilometers from the origin point"),
    db: Session = Depends(get_db)
):
    #finding near by addresses
    nearby_addresses = utils.find_nearby_addresses(
        db, latitude, longitude, distance)

    if len(nearby_addresses) == 0:
        raise HTTPException(
            status_code=404, detail="Address not found with in given distance.")
    return JSONResponse(status_code=200, content={"nearby_addresses": nearby_addresses})
