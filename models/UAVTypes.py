from sqlalchemy import Column, Integer, String
from db import BaseModelMinix, Base


class UAVType(Base, BaseModelMinix):
    __tablename__ = 'uav_types'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    model_name = Column(String)