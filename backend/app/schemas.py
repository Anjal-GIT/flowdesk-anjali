from pydantic import BaseModel, Field
from datetime import datetime
from typing import Literal


class ShipmentCreate(BaseModel):
    """Schema for creating a shipment"""
    origin: str = Field(..., min_length=1, max_length=255)
    destination: str = Field(..., min_length=1, max_length=255)
    weight_kg: float = Field(..., gt=0)


class ShipmentResponse(BaseModel):
    """Schema for shipment response"""
    id: int
    tracking_code: str
    origin: str
    destination: str
    status: Literal["pending", "in_transit", "delivered", "cancelled"]
    weight_kg: float
    created_at: datetime
    
    model_config = {
        "from_attributes": True,
    }


class ShipmentListResponse(BaseModel):
    """Paginated shipment list response"""
    items: list[ShipmentResponse]
    total: int
    page: int
    page_size: int


class ShipmentUpdate(BaseModel):
    """Schema for updating a shipment"""
    origin: str | None = Field(None, min_length=1, max_length=255)
    destination: str | None = Field(None, min_length=1, max_length=255)
    weight_kg: float | None = Field(None, gt=0)
    status: Literal["pending", "in_transit", "delivered", "cancelled"] | None = None
