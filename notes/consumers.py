# notes/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer

class NoteConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.note_id = self.scope['url_route']['kwargs']['note_id']
        self.note_group_name = f"note_{self.note_id}"
        print("Connected to note group:", self.note_group_name)
        # Join the group corresponding to the note
        await self.channel_layer.group_add(
            self.note_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave the group when the connection is closed
        await self.channel_layer.group_discard(
            self.note_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        # Receive message from WebSocket
        print("Received message:", text_data)
        data = json.loads(text_data)
        message = data['message']

        # Send message to the group
        await self.channel_layer.group_send(
            self.note_group_name,
            {
                'type': 'note_message',
                'message': message
            }
        )

    async def note_message(self, event):
        print("Sending message:", event['message'])
        # Send message to WebSocket
        message = event['message']

        await self.send(text_data=json.dumps({
            'message': message
        }))
