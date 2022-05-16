from sqlalchemy import Integer, String, ForeignKey, Column, Table
from sqlalchemy.orm import relationship
from db import BaseModelMinix, Base


association_table = Table(
    'mission-uav', Base.metadata,
    Column('uav_id', ForeignKey('uavs.id')),
    Column('mission_id', ForeignKey('missions.id'))
)


class Mission(Base, BaseModelMinix):
    __tablename__ = 'missions'

    id = Column(Integer, primary_key=True)
    start_point = Column(String)
    goal_point = Column(String)
    uavs = relationship("UAV", secondary=association_table)