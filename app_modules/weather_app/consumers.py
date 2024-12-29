import json
from app_modules.base.consumers import BaseWebsocketConsumer

class WeatherConsumer(BaseWebsocketConsumer):
    async def connect(self,**kwargs):
        await super().connect(prefix="CITY")
    
    async def disconnect(self, close_code, **kwargs):
        await super().disconnect(close_code,prefix="CITY")

    async def receive(self,**kwargs):
        await super().receive(self,**kwargs,prefix="CITY")
    