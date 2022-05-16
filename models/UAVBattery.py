from sqlalchemy import Column, Integer, Float, ForeignKey, DateTime
from db import BaseModelMinix, Base


class UAVBattery(Base, BaseModelMinix):
    __tablename__ = 'uav_battery'
    id = Column(Integer, primary_key=True)
    uav = Column(Integer, ForeignKey('uavs.id'))
    time = Column(DateTime)
    battery = Column(Float)
