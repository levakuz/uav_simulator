

class RPCCRUDMixin:

    async def create_model(self, **kwargs):
        return await self.model().create(**kwargs)

    async def delete_model(self, id: int):
        return await self.model().delete(id)

    async def update_model(self, id: int, **kwargs):
        return await self.model().update(id, **kwargs)

    async def get_model(self, id: int):
        return await self.model().get(id)
