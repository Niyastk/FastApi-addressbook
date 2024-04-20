from sqlalchemy import Column, Integer, String, Float
from db.database import Base


class Address(Base):
    """
    Model representing an address entry.

    Attributes:
        id (int): The primary key column for the ID.
        address (str): The address.
        latitude (float): The latitude coordinate.
        longitude (float): The longitude coordinate.
    """

    __tablename__ = "address"

    id = Column(Integer, primary_key=True, index=True)
    address = Column(String(200), nullable=False, index=True)
    latitude = Column(Float, nullable=False, index=True)
    longitude = Column(Float, nullable=False, index=True)
