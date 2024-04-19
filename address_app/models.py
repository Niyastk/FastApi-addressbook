from sqlalchemy import Column, Integer, String, Float
from db.database import Base

# Define the Address model
class Address(Base):
    __tablename__ = 'address'

    # Define columns for the table
    id = Column(Integer, primary_key=True, index=True)  # Primary key column for the ID
    address = Column(String(200), nullable=False, index=True)  # Column for the address
    latitude = Column(Float, nullable=False, index=True)  # Column for the latitude
    longitude = Column(Float, nullable=False, index=True)  # Column for the longitude
