import logging
import math
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.models.address import Address  
from app.schemas.address import AddressCreate, AddressUpdate

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
    
    try:
        address = Address(**payload.dict())
        db.add(address)
        db.commit()
        db.refresh(address)

        return address
    except Exception as e:
        db.rollback()
        raise

def get_address(db:Session, address_id: int) -> Address:

    address = db.query(Address).filter(Address.id == address_id).first()

    if not address:
        raise ValueError("Address not found")
    
    return address

def list_addresses(db:Session, skip: int = 0, limit: int = 100) -> List[Address]:

    return db.query(Address).offset(skip).limit(limit).all()

def update_address(db:Session, address_id: int, payload: AddressUpdate) -> Address:

    address = get_address(db, address_id)

    if not address:
        return None
    
    try:
        for field, value in payload.model_dump(exclude_unset=True).items():
            setattr(address, field, value)

        db.commit()
        db.refresh(address)
        return address
    except SQLAlchemyError as e:
        db.rollback()
        raise   

def delete_address(db:Session, address_id: int) -> None:

    address = get_address(db, address_id)

    if not address:
        return None
    
    try:
        db.delete(address)
        db.commit()
    except SQLAlchemyError as e:
        db.rollback()
        raise

def find_nearby_addresses(db:Session, latitude: float, longitude: float, radius_km: float) -> List[Address]:

    addresses = db.query(Address).all()
    nearby_addresses = []

    for address in addresses:
        distance = _haversine(latitude, longitude, address.latitude, address.longitude)
        if distance <= radius_km:
            nearby_addresses.append(address)

    return nearby_addresses