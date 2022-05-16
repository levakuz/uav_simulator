import asyncio
import datetime

from sqlalchemy import Column, Integer, String, Float, ForeignKey
from models.Mission import Mission
from models.UAVBattery import UAVBattery
from models.UAVPosition import UAVPosition
from models.UAVTrajectory import UAVTrajectory
from models.UAVTypes import UAVType
from db import Base, DBEngine, BaseModelMinix


class UAV(Base, BaseModelMinix):
    __tablename__ = 'uavs'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    flight_number = Column(String)
    fuel_resource = Column(Float)
    uav_type = Column(Integer, ForeignKey('uav_types.id'))

if __name__ == '__main__':
    engine = DBEngine()
    print(Base)
    uav = UAV()
    uav_types = UAVType()
    mission = Mission()
    asyncio.run(engine.init_models())
    a = asyncio.run(uav.get(2))
    mission.uavs.append(a)
    uavb = UAVBattery()
    uavt = UAVTrajectory()
    uavp = UAVPosition()
    asyncio.run(uavb.create(uav=2, time=datetime.datetime.now(), battery=50))
    asyncio.run(uavt.create(uav=2, time=datetime.datetime.now(), trajectory=[{'x':1, 'y': 2, 'z': 3},{'x':1, 'y': 2, 'z': 3}]))
    asyncio.run(uavp.create(uav=2, time=datetime.datetime.now(), position={'x':1, 'y': 2, 'z': 3}))
    # print(a)
    # asyncio.run(uav_types.create(name='123', model_name='123'))
    # asyncio.run(uav.create(name='123', flight_number='123', fuel_resource=123, uav_type=1))
    asyncio.run(mission.create(start_point='1', goal_point='2'))
    # asyncio.run()
    # asyncio.run(uav.delete(1))
    # asyncio.run(uav.update(2, name='33333'))