import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from django.contrib.auth import get_user_model
from . import models

User = get_user_model()

class ChatConsumer(WebsocketConsumer):

    def fetch_message(self, data):
        messages = models.Message.get_last_10_message()
        content = {
            "messages": self.get_messages_to_json(messages)
        }
        self.send(text_data=json.dumps(content))

    def new_message(self, data):
        username = "riyad"#data["from"]
        author = models.User.objects.get(username=username)
        message = models.Message.objects.create(author=author, message=data["message"])

        content = {
            "author": "riyad", #username,
            "message": message.message,
            "timestamp": str(message.timestamp)
        }

        self.send_chat_message(content)
    
    commands = {
        'fetch-message':fetch_message,
        'new-message': new_message
    }

    def get_message_to_json(self, message):
        content = {
            "author": message.author.username,
            "message": message.message,
            "timestamp": str(message.timestamp)
        }                
        return content

    def get_messages_to_json(self, messages):
        result = []
        for message in messages:
            result.append(self.get_message_to_json(message))
        
        return result 

    

    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        data = json.loads(text_data)
        self.commands[data["command"]](self, data)

        

    def send_chat_message(self, message):
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    # Receive message from room group
    def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        self.send(text_data=json.dumps(message))