from pydantic import BaseModel, Field
from datetime import datetime
from typing import Literal


class ShipmentBase(BaseModel):
    """Base Shipment schema with common fields"""
    origin: str = Field(..., min_length=1, max_length=255)
    destination: str = Field(..., min_length=1, max_length=255)
    weight_kg: float = Field(..., gt=0)
    status: Literal["pending", "in_transit", "delivered", "cancelled"] = "pending"


class ShipmentCreate(ShipmentBase):
    """Schema for creating a shipment"""
    pass


class ShipmentUpdate(BaseModel):
    """Schema for updating a shipment"""
    origin: str | None = Field(None, min_length=1, max_length=255)
    destination: str | None = Field(None, min_length=1, max_length=255)
    weight_kg: float | None = Field(None, gt=0)
    status: Literal["pending", "in_transit", "delivered", "cancelled"] | None = None


class ShipmentResponse(ShipmentBase):
    """Schema for shipment response"""
    id: int
    tracking_code: str
    created_at: datetime
    
    class Config:
        from_attributes = True


class ShipmentDetailResponse(ShipmentResponse):
    """Detailed shipment response"""
    pass
