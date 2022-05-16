from sqlalchemy import Column, Integer, ForeignKey, DateTime, JSON
from db import BaseModelMinix, Base


class UAVPosition(Base, BaseModelMinix):
    __tablename__ = 'uav_position'
    id = Column(Integer, primary_key=True)
    uav = Column(Integer, ForeignKey('uavs.id'))
    time = Column(DateTime)
    position = Column(JSON)
