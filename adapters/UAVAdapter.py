#!/usr/bin/env python3
from .AbstractAdapter import AbstractAdapter
import rospy
from uav_simulation.msgs import PointArray
from mavros.msgs import BatteryStatus


class UAVAdapter(AbstractAdapter):
    def __init__(self, rmq_username, rmq_pass, rmq_host, topics_dict, data_type, uav_id):
        AbstractAdapter.__init__(self, rmq_username, rmq_pass, rmq_host, topics_dict, data_type)
        self.uav_id = uav_id

    def create_subscribers(self):
        rospy.init_node('UAVAdapter', anonymous=True)
        rospy.Subscriber(f"{self.uav_id}/mavros/battery", BatteryStatus, self.battery_callback)
        rospy.Subscriber(f"{self.uav_id}/mavros/trajectory", PointArray, self.trajectory_callback)

    def battery_callback(self, data):
        self.send_data_from_ros_to_rmq(data.__dict__, f'{self.uav_id}/battery')

    def trajectory_callback(self, data):
        self.send_data_from_ros_to_rmq(data.__dict__, f'{self.uav_id}/trajectory')
