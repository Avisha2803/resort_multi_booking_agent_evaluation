from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base

class MenuItem(Base):
    __tablename__ = "menu_items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    price = Column(Float)
    category = Column(String) # e.g., "Main Course", "Breakfast"

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    room_number = Column(String, index=True)
    items = Column(JSON) # List of item names or IDs with quantities
    total_amount = Column(Float)
    status = Column(String, default="Pending") # Pending, Preparing, Delivered
    created_at = Column(DateTime, default=datetime.utcnow)

class ServiceRequest(Base):
    __tablename__ = "service_requests"

    id = Column(Integer, primary_key=True, index=True)
    room_number = Column(String, index=True)
    request_type = Column(String) # e.g., "Cleaning", "Towel", "Repair"
    details = Column(String, nullable=True)
    status = Column(String, default="Pending") # Pending, In Progress, Completed
    created_at = Column(DateTime, default=datetime.utcnow)
