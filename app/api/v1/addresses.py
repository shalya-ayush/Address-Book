from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.address import AddressCreate, AddressUpdate, AddressResponse
from app.services import address_service

router = APIRouter()

@router.post("/", response_model=AddressResponse)
def create_address(payload: AddressCreate, db: Session = Depends(get_db)):
    return address_service.create_address(db, payload)

@router.get("/", response_model=List[AddressResponse])
def list_addresses(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return address_service.list_addresses(db, skip, limit)

@router.get("/{address_id}", response_model=AddressResponse)
def get_address(address_id: int, db: Session = Depends(get_db)):
    try:
        return address_service.get_address(db, address_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    
@router.put("/{address_id}", response_model=AddressResponse)
def update_address(address_id: int, payload: AddressUpdate, db: Session = Depends(get_db)):
    try:
        return address_service.update_address(db, address_id, payload)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e)) 
    
@router.delete("/{address_id}", status_code=204)
def delete_address(address_id: int, db: Session = Depends(get_db)):
    try:
        address_service.delete_address(db, address_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/search/", response_model=List[AddressResponse])
def search_addresses(latitude: float  = Query(..., ge=-90,  le=90,  description="Center point latitude"),
    longitude: float = Query(..., ge=-180, le=180, description="Center point longitude"),
    distance_km: float = Query(..., gt=0, description="Search radius in kilometres"), db: Session = Depends(get_db)):
    return address_service.search_addresses(db, latitude, longitude, distance_km)