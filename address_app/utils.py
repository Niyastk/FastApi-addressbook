from sqlalchemy.orm import Session
from geopy.distance import geodesic
from . import models, schemas
from routers.address import logger


def get_address(db: Session, address_id: int):
    """
    Retrieve an address by its ID.

    Parameters:
        db (Session): SQLAlchemy database session.
        address_id (int): Identifier for the address.

    Returns:
        models.Address: The retrieved address.
    """
    try:
        return db.query(models.Address).filter(models.Address.id == address_id).first()
    except Exception as e:
        logger.error(
            f"Error occurred while retrieving address with ID {address_id}: {e}"
        )


def create_address(db: Session, address: schemas.AddressCreate):
    """
    Create a new address.

    Parameters:
        db (Session): SQLAlchemy database session.
        address (schemas.AddressCreate): Data for the new address.

    Returns:
        models.Address: The created address.
    """
    try:
        db_address = models.Address(
            address=address.address,
            latitude=address.latitude,
            longitude=address.longitude,
        )
        db.add(db_address)
        db.commit()
        db.refresh(db_address)
        logger.info(f"Created new address: {address}")
        return db_address
    except Exception as e:
        logger.error(f"Error occurred while creating address: {e}")


def get_address_by_coordinates(db: Session, latitude: str, longitude: str):
    """
    Retrieve an address by its coordinates.

    Parameters:
        db (Session): SQLAlchemy database session.
        latitude (str): Latitude of the address.
        longitude (str): Longitude of the address.

    Returns:
        models.Address: The retrieved address.
    """
    try:
        return (
            db.query(models.Address)
            .filter(
                models.Address.latitude == latitude,
                models.Address.longitude == longitude,
            )
            .first()
        )
    except Exception as e:
        logger.error(
            f"Error occurred while retrieving address by coordinates ({latitude}, {longitude}): {e}"
        )


def get_all_addresses(db: Session):
    """
    Retrieve all addresses.

    Parameters:
        db (Session): SQLAlchemy database session.

    Returns:
        List[models.Address]: List of all addresses.
    """
    try:
        return db.query(models.Address).all()
    except Exception as e:
        logger.error(f"Error occurred while retrieving all addresses: {e}")


def update_address(db: Session, address_id: int, address: schemas.AddressUpdate):
    """
    Update an address with given values.

    Parameters:
        db (Session): SQLAlchemy database session.
        address_id (int): Identifier for the address to be updated.
        address (schemas.AddressUpdate): Data to update the address.

    Returns:
        models.Address: The updated address.
    """
    try:
        db_address = db.query(models.Address).get(address_id)
        if db_address:
            for key, value in address.dict(exclude_unset=True).items():
                setattr(db_address, key, value)
            db.commit()
            db.refresh(db_address)
            logger.info(f"Updated address with ID {address_id}: {address}")
        return db_address
    except Exception as e:
        logger.error(f"Error occurred while updating address with ID {address_id}: {e}")


def delete_address(db: Session, address_id: int):
    """
    Delete an address.

    Parameters:
        db (Session): SQLAlchemy database session.
        address_id (int): Identifier for the address to be deleted.

    Returns:
        models.Address: The deleted address.
    """
    try:
        db_address = db.query(models.Address).get(address_id)
        if db_address:
            db.delete(db_address)
            db.commit()
            logger.info(f"Deleted address with ID {address_id}")
        return db_address
    except Exception as e:
        logger.error(f"Error occurred while deleting address with ID {address_id}: {e}")


def find_nearby_addresses(db, latitude, longitude, distance):
    """
    Find nearby addresses within a given distance from a specified location.

    Parameters:
        db (Session): SQLAlchemy database session.
        latitude (float): Latitude of the specified location.
        longitude (float): Longitude of the specified location.
        distance (float): Maximum distance to search for nearby addresses (in kilometers).

    Returns:
        List[Dict[str, Union[int, str, float]]]: List of nearby addresses with their details.
    """
    try:
        addresses = get_all_addresses(db)
        nearby_addresses = []
        origin_point = (latitude, longitude)
        for address in addresses:
            address_point = (address.latitude, address.longitude)
            dist_km = geodesic(origin_point, address_point).kilometers
            if dist_km <= distance:
                nearby_addresses.append(
                    {
                        "id": address.id,
                        "address": address.address,
                        "latitude": address.latitude,
                        "longitude": address.longitude,
                    }
                )
        return nearby_addresses
    except Exception as e:
        logger.error(f"Error occurred while finding nearby addresses: {e}")
