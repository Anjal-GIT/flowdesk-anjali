from sqlalchemy import Column, Integer, String, Float, DateTime, Enum
from sqlalchemy.sql import func
from app.database import Base
from enum import Enum as PyEnum
from datetime import datetime
import uuid
from datetime import datetime


class ShipmentStatus(PyEnum):
    """Shipment status enumeration"""
    PENDING = "pending"
    IN_TRANSIT = "in_transit"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"


class Shipment(Base):
    """SQLAlchemy model for Shipment"""
    
    __tablename__ = "shipments"
    
    id = Column(Integer, primary_key=True, index=True)
    tracking_code = Column(String(50), unique=True, nullable=False, index=True)
    origin = Column(String(255), nullable=False)
    destination = Column(String(255), nullable=False)
    status = Column(
        Enum(ShipmentStatus),
        default=ShipmentStatus.PENDING,
        nullable=False
    )
    weight_kg = Column(Float, nullable=False)
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )
    
    def __repr__(self):
        return f"<Shipment(id={self.id}, tracking_code='{self.tracking_code}', status='{self.status.value}')>"
