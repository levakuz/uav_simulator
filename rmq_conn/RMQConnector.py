import asyncio
import json
from abc import abstractmethod

from aio_pika import connect_robust, Message
from aio_pika.abc import AbstractIncomingMessage
from aio_pika.patterns import RPC


class AbstractConnector:
    def __init__(
            self,
            rmq_username,
            rmq_pass,
            rmq_host,
            model
    ):
        self.rmq_username = rmq_username
        self.rmq_pass = rmq_pass
        self.rmq_host = rmq_host
        self.model = model

    async def async_init(self):
        self.connection = await connect_robust(
            f"amqp://{self.rmq_username}:{self.rmq_pass}@{self.rmq_host}/"
        )
        self.channel = await self.connection.channel()
        self.exchange = self.channel.default_exchange
        await self.create_rpc_queues()
        await self.run()

    def __await__(self):
        return self.async_init().__await__()

    async def create_rpc_queues(self):
        queue = await self.channel.declare_queue(f'get_{self.model.__name__}')
        await queue.consume(self.get)
        queue = await self.channel.declare_queue(f'delete_{self.model.__name__}')
        await queue.consume(self.delete)
        queue = await self.channel.declare_queue(f'create_{self.model.__name__}')
        await queue.consume(self.create)
        queue = await self.channel.declare_queue(f'edit_{self.model.__name__}')
        await queue.consume(self.edit)

    async def create(self, message: AbstractIncomingMessage) -> None:
        await message.ack()
        result = await self.create_model(**json.loads(message.body))
        await self.exchange.publish(
            Message(
                body=json.dumps(result).encode(),
                correlation_id=message.correlation_id,
            ),
            routing_key=message.reply_to,
        )

    async def get(self, message: AbstractIncomingMessage):
        await message.ack()
        model = await self.get_model(json.loads(message.body))
        answer = {}
        for key, val in model.__dict__.items():
            if key == 'time':
                answer[key] = val.strftime("%Y-%m-%d %H:%M:%S")
            elif key[0] != '_':
                answer[key] = val
        await self.exchange.publish(
            Message(
                body=json.dumps(answer).encode(),
                correlation_id=message.correlation_id,
            ),
            routing_key=message.reply_to,
        )

    async def delete(self, message: AbstractIncomingMessage):
        await message.ack()
        result = await self.delete_model(json.loads(message.body))
        await self.exchange.publish(
            Message(
                body=json.dumps({'count': result.rowcount}).encode(),
                correlation_id=message.correlation_id,
            ),
            routing_key=message.reply_to,
        )

    async def edit(self, message: AbstractIncomingMessage):
        await message.ack()
        new_data = json.loads(message.body)
        result = await self.update_model(**new_data)
        await self.exchange.publish(
            Message(
                body=json.dumps({'count': result.rowcount}).encode(),
                correlation_id=message.correlation_id,
            ),
            routing_key=message.reply_to,
        )

    async def run(self):
        try:
            await asyncio.Future()
        finally:
            await self.connection.close()

