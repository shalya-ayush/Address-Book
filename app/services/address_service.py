import logging
import math
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.models.address import Address  
from app.schemas.address import AddressCreate, AddressUpdate

logger = logging.getLogger(__name__)

EARTH_RADIUS_KM = 6371

def _haversine(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Calculate the great circle distance in kilometers between two points
    """
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)

    a = math.sin(delta_phi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2) ** 2

    c = math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return EARTH_RADIUS_KM * c



def create_address(db:Session, payload: AddressCreate) -> Address:
    
    logger.info(f"Creating address with name: {payload.name}")
    try:
        address = Address(**payload.dict())
        db.add(address)
        db.commit()
        db.refresh(address)
        logger.info(f"Address created with name: {address.name}, id: {address.id}")

        return address
    except Exception as e:
        db.rollback()
        logger.error("Error creating address: %s", e)
        raise

def get_address(db:Session, address_id: int) -> Address:

    logger.info(f"Retrieving address with id: {address_id}")

    address = db.query(Address).filter(Address.id == address_id).first()

    if not address:
        logger.warning(f"Address with id {address_id} not found")
        raise ValueError("Address not found")
    
    logger.info(f"Address retrieved with id: {address_id}, name: {address.name}")
    return address

def list_addresses(db:Session, skip: int = 0, limit: int = 100) -> List[Address]:

    logger.info(f"Listing addresses with skip: {skip}, limit: {limit}")

    return db.query(Address).offset(skip).limit(limit).all()

def update_address(db:Session, address_id: int, payload: AddressUpdate) -> Address:

    logger.info(f"Updating address with id: {address_id}")

    address = get_address(db, address_id)

    if not address:
        logger.warning(f"Address with id {address_id} not found for update")
        return None
    
    try:
        for field, value in payload.model_dump(exclude_unset=True).items():
            setattr(address, field, value)

        db.commit()
        db.refresh(address)
        logger.info(f"Address updated with id: {address_id}, name: {address.name}")
        return address
    except SQLAlchemyError as e:
        db.rollback()
        logger.error("Error updating address with id %s: %s", address_id, e)
        raise   

def delete_address(db:Session, address_id: int) -> None:

    logger.info(f"Deleting address with id: {address_id}")

    address = get_address(db, address_id)

    if not address:
        logger.warning(f"Address with id {address_id} not found for deletion")
        return None
    
    try:
        db.delete(address)
        db.commit()
        logger.info(f"Address deleted with id: {address_id}, name: {address.name}")
    except SQLAlchemyError as e:
        db.rollback()
        logger.error("Error deleting address with id %s: %s", address_id, e)
        raise

def find_nearby_addresses(db:Session, latitude: float, longitude: float, radius_km: float) -> List[Address]:

    logger.info(f"Finding nearby addresses for lat: {latitude}, lon: {longitude}, radius: {radius_km} km")

    addresses = db.query(Address).all()
    nearby_addresses = []

    for address in addresses:
        distance = _haversine(latitude, longitude, address.latitude, address.longitude)
        logger.info(f"Distance to {address.name} is {distance:.2f} km for address id: {address.id}")
        if distance <= radius_km:
            nearby_addresses.append(address)

    logger.info(f"Found {len(nearby_addresses)} nearby addresses")
    return nearby_addresses
