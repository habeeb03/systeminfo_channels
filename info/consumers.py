from channels.generic.websocket import AsyncWebsocketConsumer
import json
import psutil


class UpdateSystemInfo(AsyncWebsocketConsumer):

    async def connect(self):
        self.room_name = 'test_room'
        self.group_name = 'test_group'

        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name,
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def recive(self, text_data):  
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        print(message)

        # Send message to room group
        await self.channel_layer.group_send(
            self.group_name,
            {
                'type': 'system_load',
                'data': {
                    'cpu_percent': psutil.cpu_percent(),  # initial value for cpu and ram set to 0
                    'ram_percent': psutil.virtual_memory().percent
                }
            }
        )

    async def system_load(self, event):
        print(event)
        await self.send(text_data=json.dumps(event['data']))

        