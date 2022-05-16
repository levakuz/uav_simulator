import asyncio

from rmq_conn import RPCCRUDMixin, AbstractConnector
from models import UAVBattery


class UAVBatteryRPCHandler(AbstractConnector, RPCCRUDMixin):
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
            UAVBattery
        )

async def main():
    await UAVBatteryRPCHandler('guest', 'guest', 'localhost')

if __name__ == '__main__':
    asyncio.run(main())