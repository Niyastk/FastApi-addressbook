from fastapi import APIRouter, HTTPException, Depends, Query
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from db.database import SessionLocal
from loguru import logger
from address_app import utils, schemas


# Configure Loguru to write logs to a file named app.log
logger.add("app.log", rotation="500 MB", retention="10 days", level="DEBUG")


router = APIRouter(tags=["Address CRUD Operations"])


def get_db():
    """
    Retrieve a database session.

    Yields:
        Session: A SQLAlchemy database session.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/addresses/", response_model=schemas.Address, status_code=201)
def create_address(address: schemas.AddressCreate, db: Session = Depends(get_db)):
    """
    Create a new address.

    Parameters:
        address (schemas.AddressCreate): Data for the new address.
        db (Session, optional): SQLAlchemy database session. Defaults to Depends(get_db).

    Returns:
        schemas.Address: The created address.
    """
    db_address = utils.get_address_by_coordinates(
        db=db, latitude=address.latitude, longitude=address.longitude
    )
    if db_address:
        logger.error("Address already exists.")
        raise HTTPException(status_code=400, detail="Address already exists.")

    # Log the creation of a new address
    logger.info(f"Creating new address: {address}")

    return utils.create_address(db, address=address)


@router.get("/addresses_all/", response_model=list[schemas.Address])
def list_addresses(db: Session = Depends(get_db)):
    """
    Get all addresses.

    Parameters:
        db (Session, optional): SQLAlchemy database session. Defaults to Depends(get_db).

    Returns:
        List[schemas.Address]: List of all addresses.
    """
    addresses = utils.get_all_addresses(db)
    if len(addresses) == 0:
        logger.error("No addresses found in database.")
        raise HTTPException(status_code=404, detail="No addresses found in database.")
    return addresses


@router.get("/addresses/{address_id}", response_model=schemas.Address)
def get_address_by_id(address_id: int, db: Session = Depends(get_db)):
    """
    Get a single address by its ID.

    Parameters:
        address_id (int): Identifier for the address.
        db (Session, optional): SQLAlchemy database session. Defaults to Depends(get_db).

    Returns:
        schemas.Address: The retrieved address.
    """
    address = utils.get_address(db=db, address_id=address_id)
    if address is None:
        logger.error(f"Address with ID {address_id} not found.")
        raise HTTPException(status_code=404, detail="Address not found.")
    return address


@router.put("/addresses/{address_id}", response_model=schemas.Address)
def update_address(
    address_id: int, address: schemas.AddressUpdate, db: Session = Depends(get_db)
):
    """
    Update an address.

    Parameters:
        address_id (int): Identifier for the address to be updated.
        address (schemas.AddressUpdate): Data to update the address.
        db (Session, optional): SQLAlchemy database session. Defaults to Depends(get_db).

    Returns:
        schemas.Address: The updated address.
    """
    db_address = utils.get_address(db=db, address_id=address_id)
    if db_address is None:
        logger.error(f"Address with ID {address_id} not found.")
        raise HTTPException(status_code=404, detail="Address not found.")

    # Log the update of an address
    logger.info(f"Updating address with ID {address_id}: {address}")

    return utils.update_address(db=db, address_id=address_id, address=address)


@router.delete("/addresses/{address_id}", response_model=schemas.Address)
def delete_address(address_id: int, db: Session = Depends(get_db)):
    """
    Delete an address.

    Parameters:
        address_id (int): Identifier for the address to be deleted.
        db (Session, optional): SQLAlchemy database session. Defaults to Depends(get_db).

    Returns:
        schemas.Address: The deleted address.
    """
    db_address = utils.get_address(db=db, address_id=address_id)
    if db_address is None:
        logger.error(f"Address with ID {address_id} not found.")
        raise HTTPException(status_code=404, detail="Address not found.")

    # Log the deletion of an address
    logger.info(f"Deleting address with ID {address_id}")

    return utils.delete_address(db=db, address_id=address_id)


@router.get(
    "/nearby_addresses", response_model=schemas.Address, tags=["Nearby Address"]
)
def get_nearby_addresses(
    latitude: float = Query(..., description="Latitude of the origin point"),
    longitude: float = Query(..., description="Longitude of the origin point"),
    distance: float = Query(
        ..., description="Maximum distance in kilometers from the origin point"
    ),
    db: Session = Depends(get_db),
):
    """
    Get nearby addresses within a given distance from a specified location.

    Parameters:
        latitude (float): Latitude of the origin point.
        longitude (float): Longitude of the origin point.
        distance (float): Maximum distance in kilometers from the origin point.
        db (Session, optional): SQLAlchemy database session. Defaults to Depends(get_db).

    Returns:
        JSONResponse: Response containing nearby addresses.
    """
    # Log the request for nearby addresses
    logger.info(
        f"Finding nearby addresses around ({latitude}, {longitude}) within {distance} km"
    )

    nearby_addresses = utils.find_nearby_addresses(db, latitude, longitude, distance)

    if len(nearby_addresses) == 0:
        logger.error("No addresses found within the given distance.")
        raise HTTPException(
            status_code=404, detail="No addresses found within the given distance."
        )

    # Log the found nearby addresses
    logger.info(f"Found nearby addresses: {nearby_addresses}")

    return JSONResponse(status_code=200, content={"nearby_addresses": nearby_addresses})
