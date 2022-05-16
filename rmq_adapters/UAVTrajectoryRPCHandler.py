from rmq_conn import RPCCRUDMixin, AbstractConnector
from models import UAVTrajectory


class UAVTrajectoryRPCHandler(AbstractConnector, RPCCRUDMixin):
    def __init__(
            self,
            rmq_username,
            rmq_pass,
            rmq_host
    ):
        AbstractConnector.__init__(
            self,
            rmq_username,
            rmq_pass,
            rmq_host,
            UAVTrajectory
        )
