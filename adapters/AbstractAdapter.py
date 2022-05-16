#!/usr/bin/env python3
import json
import rospy
from std_msgs.msg import String
import pika


class AbstractAdapter:
    def __init__(self, rmq_username, rmq_pass, rmq_host, topics_dict, data_type):
        self.rmq_username = rmq_username
        self.rmq_pass = rmq_pass
        self.rmq_host = rmq_host
        self.topics_dict = topics_dict
        self.exchange = data_type
        self.create_subscribers()
        self.credentials = pika.PlainCredentials(self.rmq_username, self.rmq_pass)
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(self.rmq_host,
                                                                            5672,
                                                                            '/',
                                                                            self.credentials,
                                                                            blocked_connection_timeout=0,
                                                                            heartbeat=0))
        self.channel = self.connection.channel()
        self.channel.exchange_declare(
            self.exchange,
            exchange_type='topic',
            passive=False,
            durable=False,
            auto_delete=False,
            arguments=None
        )

    def create_subscribers(self):
        pass

    def send_data_from_ros_to_rmq(self, data, routing_key):
        self.channel.basic_publish(
            exchange=self.exchange,
            routing_key=routing_key,
            body=json.dumps(data),
            properties=pika.BasicProperties(
                delivery_mode=2,
            )
        )

    def run(self):
        rospy.spin()
