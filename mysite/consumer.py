import json
from channels.db import database_sync_to_async
from djangochannelsrestframework.observer.generics import GenericAsyncAPIConsumer

from mysite.models import Room, Message, Profile


class RoomConsumer(GenericAsyncAPIConsumer):
    async def connect(self):
        self.room_id = self.scope['url_route']['kwargs']['pk'] # Извлечение 'pk' из параметров URL, переданных в маршруте
        self.room_group_name = f'chat_{self.room_id}'
        self.room = await self.get_room(self.room_id)

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        messages = await self.all_messages_in_room(self.room_id)
        for message in messages:
            await self.send(text_data=json.dumps({
                'message': message.text,
                'profile': message.profile.id,
                'created_at': message.created_at
            }))
        await self.accept()

    async def disconnect(self, code):
        # await self.channel_layer.group_discard(
        #     self.room_group_name,
        #     self.channel_name
        # )
        pass

    #receive: Когда пользователь отправляет сообщение через WebSocket,
    # этот метод получает текстовые данные, создает новое сообщение в базе данных и отправляет его всем пользователям
    # в группе каналов комнаты чата.
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = str(text_data_json['message'])
        try:
            profile = int(text_data_json['profile'])
        except ValueError:
            await self.send(text_data=json.dumps({
                'error': 'Invalid profile ID'
            }))
            return

        created_at = await self.create_message(self.room, message, profile)
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_room',
                'message': message,
                'profile': profile,
                'created_at': created_at.isoformat(), # Преобразование в строку формата ISO 8601
            }
        )

    #chat_room: Этот метод вызывается, когда сообщение отправляется группе каналов.
    # Он отправляет сообщение всем подключенным пользователям.
    async def chat_room(self, event):
        message = str(event['message'])
        profile = int(event['profile'])
        await self.send(text_data=json.dumps({
            'message': message,
            'profile': profile,

        }))

    @database_sync_to_async
    def get_room(self, pk):
        return Room.objects.get(pk=pk)

    @database_sync_to_async
    def all_messages_in_room(self, room_pk):
        room = Room.objects.get(pk=room_pk)
        return list(Message.objects.filter(room=room)) #Этот метод возвращает QuerySet,
        # который является ленивым и не выполняет запрос к базе данных до тех пор,
        # пока не будет вызвана итерация или другая операция, требующая выполнения запроса.Нужен лист из сообщений!!!!!!!

    @database_sync_to_async
    def create_message(self, room, profile_id, message):
        profile = Profile.objects.get(pk=profile_id)
        new_message = Message.objects.create(text=message, profile=profile, room=room)
        return new_message.created_at
