from .database import Base
from sqlalchemy import DateTime, Column, Integer, String, TIMESTAMP, text, Boolean, ForeignKey, Text, Float
from sqlalchemy.orm import relationship
from typing import Optional
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, nullable=False, primary_key=True)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'),
                        nullable=False)
    # Define the one-to-many relationship between User and Invoice
    invoices = relationship("Invoice", back_populates="user")


class Invoice(Base):
    __tablename__ = "invoices"

    id = Column(Integer, nullable=False, primary_key=True)
    order_number = Column(String, nullable=False, unique=True)
    title = Column(String, nullable=False)
    cost_per_page = Column(Float, default=0.0)  # Optional
    pages_done = Column(Integer, nullable=False)
    total_amount_per_job = Column(Float, nullable=False)
    total_amount_for_all_jobs = Column(Float, nullable=False)
    paid_amount = Column(Float, default=0.0)
    advance_amount = Column(Float, default=0.0)
    remaining = Column(Float, nullable=False)
    due_date = Column(DateTime, nullable=False)
    job_status = Column(Boolean, default=False)  # Complete or not
    order_status = Column(Boolean, default=False)  # Approved or cancelled
    
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    user = relationship("User", back_populates="invoices")
