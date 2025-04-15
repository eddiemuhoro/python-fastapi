from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base
from datetime import datetime

class Deployments(Base):
    __tablename__ = "deployments"

    id = Column(Integer, primary_key=True, index=True)
    lat = Column(Float, nullable=True)
    lng = Column(Float, nullable=True)
    date_registered = Column(DateTime, default=datetime.utcnow)

    discharge_data = relationship("DischargeData", back_populates="deployment")
    alerts = relationship("Alerts", back_populates="deployment")

class DischargeData(Base):
    __tablename__ = "discharge_data"

    id = Column(Integer, primary_key=True, index=True)
    application_id = Column(String(255), nullable=False)
    received_at = Column(DateTime, nullable=False)
    distance = Column(Float, nullable=False)
    level = Column(Float, nullable=True)
    pulse = Column(Float, nullable=False)
    flow_rate = Column(Float, nullable=False)
    voltage_battery = Column(Float, nullable=False)
    voltage_solar = Column(Float, nullable=False)
    temp = Column(Float, nullable=True)
    voltage_temp = Column(Float, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    device_id = Column(Integer, ForeignKey("deployments.id"), nullable=True)
    deployment = relationship("Deployments", back_populates="discharge_data")


class Alerts(Base):
    __tablename__ = "alerts"

    alert_id = Column(Integer, primary_key=True, index=True)  # Primary key
    level = Column(Float, nullable=False)  # Level
    message = Column(String, nullable=False)  # Alert message
    alert_time = Column(DateTime, default=datetime.utcnow)  # Time of the alert
    abstractor_name = Column(String, nullable=True)  # Abstractor's name
    abstractor_phone = Column(String, nullable=True)  # Abstractor's phone number
    catchment = Column(String, nullable=True)  # Catchment area
    alertType = Column(String, nullable=False)  # Type of alert

    device_id = Column(Integer, ForeignKey("deployments.id"), nullable=True)  # Foreign key to deployments table
    deployment = relationship("Deployments", back_populates="alerts")
    
    