from sqlalchemy import Column, Integer, ForeignKey, DateTime, JSON
from db import BaseModelMinix, Base


class UAVTrajectory(Base, BaseModelMinix):
    __tablename__ = 'uav_trajectory'
    id = Column(Integer, primary_key=True)
    uav = Column(Integer, ForeignKey('uavs.id'))
    time = Column(DateTime)
    trajectory = Column(JSON)
