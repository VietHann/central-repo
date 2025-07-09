from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

# Replace with your database URL
DATABASE_URL = 'sqlite:///smarthome.db'

engine = create_engine(DATABASE_URL)
Base = declarative_base()

class Device(Base):
    __tablename__ = 'devices'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    type = Column(String)
    status = Column(String)

class EnergyUsage(Base):
    __tablename__ = 'energy_usage'

    id = Column(Integer, primary_key=True)
    device_id = Column(Integer)
    usage = Column(Float)
    timestamp = Column(DateTime, default=datetime.utcnow)

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()