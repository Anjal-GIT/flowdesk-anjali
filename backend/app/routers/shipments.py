from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime
from app.database import get_db
from app.models import Shipment, ShipmentStatus
from app.schemas import ShipmentCreate, ShipmentUpdate, ShipmentResponse, ShipmentDetailResponse
from app.dependencies import verify_api_key
import uuid

router = APIRouter(
    prefix="/shipments",
    tags=["shipments"],
)


def generate_tracking_code() -> str:
    """
    Generate a unique tracking code in format: SHP-YYYYMMDD-XXXXX
    
    Returns:
        A formatted tracking code string
    """
    now = datetime.utcnow()
    date_part = now.strftime("%Y%m%d")
    # Generate 5-character random hex string
    random_part = uuid.uuid4().hex[:5].upper()
    return f"SHP-{date_part}-{random_part}"


@router.post(
    "/",
    response_model=ShipmentResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new shipment"
)
async def create_shipment(
    shipment: ShipmentCreate,
    db: Session = Depends(get_db),
    api_key: str = Depends(verify_api_key),
):
    """
    Create a new shipment.
    
    **Required Header:**
    - X-API-Key: Your API key
    
    **Request body:**
    - origin: Shipment origin location
    - destination: Shipment destination location
    - weight_kg: Weight in kilograms
    - status: Shipment status (optional, defaults to 'pending')
    
    **Returns:**
    - Created shipment with auto-generated tracking code
    """
    tracking_code = generate_tracking_code()
    
    db_shipment = Shipment(
        tracking_code=tracking_code,
        origin=shipment.origin,
        destination=shipment.destination,
        weight_kg=shipment.weight_kg,
        status=ShipmentStatus(shipment.status),
    )
    
    db.add(db_shipment)
    db.commit()
    db.refresh(db_shipment)
    
    return db_shipment


@router.get(
    "/",
    response_model=list[ShipmentResponse],
    summary="List all shipments"
)
async def list_shipments(
    db: Session = Depends(get_db),
    api_key: str = Depends(verify_api_key),
    skip: int = 0,
    limit: int = 100,
):
    """
    Retrieve all shipments with pagination.
    
    **Required Header:**
    - X-API-Key: Your API key
    
    **Query parameters:**
    - skip: Number of records to skip (default: 0)
    - limit: Maximum records to return (default: 100)
    """
    shipments = db.query(Shipment).offset(skip).limit(limit).all()
    return shipments


@router.get(
    "/{shipment_id}",
    response_model=ShipmentDetailResponse,
    summary="Get shipment by ID"
)
async def get_shipment(
    shipment_id: int,
    db: Session = Depends(get_db),
    api_key: str = Depends(verify_api_key),
):
    """
    Retrieve a specific shipment by ID.
    
    **Required Header:**
    - X-API-Key: Your API key
    
    **Path parameters:**
    - shipment_id: The shipment's unique identifier
    """
    shipment = db.query(Shipment).filter(Shipment.id == shipment_id).first()
    
    if not shipment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Shipment with id {shipment_id} not found",
        )
    
    return shipment


@router.get(
    "/tracking/{tracking_code}",
    response_model=ShipmentDetailResponse,
    summary="Get shipment by tracking code"
)
async def get_shipment_by_tracking(
    tracking_code: str,
    db: Session = Depends(get_db),
    api_key: str = Depends(verify_api_key),
):
    """
    Retrieve a shipment by tracking code.
    
    **Required Header:**
    - X-API-Key: Your API key
    
    **Path parameters:**
    - tracking_code: The shipment's tracking code (e.g., SHP-20240115-ABC12)
    """
    shipment = db.query(Shipment).filter(Shipment.tracking_code == tracking_code).first()
    
    if not shipment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Shipment with tracking code '{tracking_code}' not found",
        )
    
    return shipment


@router.patch(
    "/{shipment_id}",
    response_model=ShipmentDetailResponse,
    summary="Update shipment"
)
async def update_shipment(
    shipment_id: int,
    shipment_update: ShipmentUpdate,
    db: Session = Depends(get_db),
    api_key: str = Depends(verify_api_key),
):
    """
    Update a shipment's information.
    
    **Required Header:**
    - X-API-Key: Your API key
    
    **Path parameters:**
    - shipment_id: The shipment's unique identifier
    
    **Request body:** (all fields optional)
    - origin: Updated origin location
    - destination: Updated destination location
    - weight_kg: Updated weight
    - status: Updated status
    """
    db_shipment = db.query(Shipment).filter(Shipment.id == shipment_id).first()
    
    if not db_shipment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Shipment with id {shipment_id} not found",
        )
    
    update_data = shipment_update.model_dump(exclude_unset=True)
    
    for field, value in update_data.items():
        if field == "status" and value is not None:
            setattr(db_shipment, field, ShipmentStatus(value))
        else:
            setattr(db_shipment, field, value)
    
    db.add(db_shipment)
    db.commit()
    db.refresh(db_shipment)
    
    return db_shipment


@router.delete(
    "/{shipment_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete shipment"
)
async def delete_shipment(
    shipment_id: int,
    db: Session = Depends(get_db),
    api_key: str = Depends(verify_api_key),
):
    """
    Delete a shipment.
    
    **Required Header:**
    - X-API-Key: Your API key
    
    **Path parameters:**
    - shipment_id: The shipment's unique identifier
    """
    db_shipment = db.query(Shipment).filter(Shipment.id == shipment_id).first()
    
    if not db_shipment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Shipment with id {shipment_id} not found",
        )
    
    db.delete(db_shipment)
    db.commit()
