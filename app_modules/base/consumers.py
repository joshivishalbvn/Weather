import json , re
from channels.layers import get_channel_layer
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer


class BaseWebsocketConsumer(AsyncWebsocketConsumer):

    channel_layer = get_channel_layer()
    group_name = ""

    async def connect(self, **kwargs):
        prefix = kwargs.get("prefix", "weather")

        try:
            self.id = self.scope.get("url_route", {}).get("kwargs", {}).get("city", None)
            self.group_name = f"{prefix}_{self.id}" if self.id else prefix
            # self.group_name = self.sanitize_group_name(self.group_name)
            print('\033[91m'+'self.group_name: ' + '\033[92m', self.group_name)
            await self.channel_layer.group_add(self.group_name, self.channel_name)
            await self.accept()
        except Exception as e:
            print(f'\033[91mError in connect: \033[92m{e}')
            await self.close()

    async def disconnect(self, close_code, **kwargs):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def broadcast_message(self, event):
        message = event["message"]
        try:
            await self.send(text_data=json.dumps(message))
        except Exception as e:
            print('\033[91m'+'Error in broadcast_message: ' + '\033[92m', e)
            await self.close()

    def sanitize_group_name(self,group_name):
        return re.sub(r'[^a-zA-Z0-9._-]', '_', group_name)

    async def receive(self, bytes_data=None, **kwargs):
        text_data = kwargs.get("text_data")
        bytes_data = kwargs.get("bytes_data")  # noqa
        try:
            data = json.loads(text_data)
        except json.JSONDecodeError:
            data = text_data

        if data == "ping":
            data = "pong"

        await self.channel_layer.group_send(self.group_name, {"type": "broadcast_message", "message": data})