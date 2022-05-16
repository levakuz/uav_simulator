#!/usr/bin/env python3

from .AbstractAdapter import AbstractAdapter
import rospy
from geometry_msgs.msg import PoseStamped
from sensor_msgs.msg import NavSatFix

class GEOAdapter(AbstractAdapter):
    def __init__(self, rmq_username, rmq_pass, rmq_host, topics_dict):
        AbstractAdapter.__init__(self, rmq_username, rmq_pass, rmq_host, topics_dict, 'Geoposition')

    def create_subscribers_for_uav(self, uav_id):
        rospy.init_node('GEOAdapter', anonymous=True)
        rospy.Subscriber(f"/mavros/local_position/{uav_id}", PoseStamped, self.local_position_callback)
        rospy.Subscriber(f"/mavros/global_position/{uav_id}", NavSatFix, self.global_position_callback)

    def local_position_callback(self, data):
        self.send_data_from_ros_to_rmq(data.__dict__, 'local_position')
    def global_position_callback(self, data):
        self.send_data_from_ros_to_rmq(data.__dict__, 'global_position')