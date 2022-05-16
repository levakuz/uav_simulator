#!/usr/bin/env python3
from .AbstractAdapter import AbstractAdapter
import rospy
from geometry_msgs.msgs import PoseStamped
from sensor_msgs.msgs import NavSatFix
from physics_msgs.msgs import Wind

class EnvironmentAdapter(AbstractAdapter):
    def __init__(self, rmq_username, rmq_pass, rmq_host, topics_dict):
        AbstractAdapter.__init__(self, rmq_username, rmq_pass, rmq_host, topics_dict, 'environment')

    def create_subscribers_for_uav(self, uav_id):
        rospy.init_node('EnvironmentAdapter', anonymous=True)
        rospy.Subscriber("/world_wind/", Wind, self.wind_callback)

    def wind_callback(self, data):
        self.send_data_from_ros_to_rmq(data.__dict__, 'wind')