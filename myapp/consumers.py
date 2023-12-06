from channels.consumer import SyncConsumer,AsyncConsumer
from channels.exceptions import StopConsumer
import json
from asgiref.sync import async_to_sync
from django.contrib.auth.models import User
from .models import Group,Chat,Onlineuser


class MySyncConsumer(SyncConsumer):
    def websocket_connect(self, event):
        channel_layer = self.channel_layer
        channel_name = self.channel_name
        user_id = self.scope["session"]["_auth_user_id"] #to get this use Authintication in Channels
        # self.groupName = self.scope['url_route']['kwargs']['gropkaname']
        # grouppname = self.groupName
        # print('This is a group nammmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm',grouppname)
        self.recipient_idd = self.scope['url_route']['kwargs']['chat_with']
 


   
        group = f'chat_{min(int(user_id),int(self.recipient_idd))}_{max(int(user_id),int(self.recipient_idd))}'

        async_to_sync(channel_layer.group_add)(group,channel_name)

        
        #accept the connect
        self.send({
            'type':'websocket.accept'
        })

        self.user_id = user_id  # i set user_id as self so that i can use accross other methods
        self.channel_layer = channel_layer
        self.channel_name = channel_name
        self.group = group


    def websocket_receive(self, event):        
        data = json.loads(event['text'])     

        user_id = self.user_id

        # database data
        sender = User.objects.get(id = user_id)
        recipientt = data['receiver']

        person_geting_data = User.objects.get(username=recipientt)


        recipient_id = person_geting_data.id
        user_id = self.user_id
        user = self.scope['user']
   


        async_to_sync(self.channel_layer.group_add)(self.group,self.channel_name)

        to_group = Group.objects.get(name=self.group)

        chat = Chat(
            name = sender,
            recipient = person_geting_data,
            group= to_group,
            content = data['msg'],
        )

        chat.save()


        async_to_sync(self.channel_layer.group_send)(self.group,{'type':'chat.message','message':data['msg'],'sender_id': user_id,})


    def chat_message(self,event):
        sender_id = event['sender_id']
        current_user_id = self.user_id
        message_class = 'message sent' if sender_id == current_user_id else 'message received'
        message = {'message':event['message'],'class':message_class}
        self.send({'type':'websocket.send','text':json.dumps(message)})


    def websocket_disconnect(self, event):
        print('Websocket disconnected...', event)
        async_to_sync(self.channel_layer.group_discard)(self.group,self.channel_name)
        raise StopConsumer()


    


#Please Avoid Async class im doing with sync..

class MyAsyncConsumer(AsyncConsumer):

    async def websocket_connect(self, event):

        #accept the connect
        await self.send({
            'type':'websocket.accept'
        })

    async def websocket_receive(self, event):
        await self.send({
            'type':'websocket.send',
            'text':'hello'
        })

    async def websocket_disconnect(self, event):
        raise StopConsumer()








#Online | Offline status Consumers...

class OnlineStatusConsumer(SyncConsumer):
    def websocket_connect(self,event):
        print('Websocket status has been connected...')
        self.room_group_name = 'user'
        group = self.room_group_name
        channel_layer = self.channel_layer
        channel_name = self.channel_name

        async_to_sync(channel_layer.group_add)(group,channel_name)
        self.send({'type':'websocket.accept'})

    def websocket_receive(self, event):
        parsed_data = json.loads(event['text'])
        username = parsed_data['username']
        connection_type = parsed_data['type']
        
        try:
            user = User.objects.get(username=username)
            # Assuming Onlineuser has a foreign key 'user' pointing to the User model
            status_user = Onlineuser.objects.get(user=user)
            
            if connection_type == 'open':
                status_user.is_online = True
                status_user.save()
            else:
                status_user.is_online = False
                status_user.save()
        except User.DoesNotExist:
            # Handle the case when the user does not exist
            print('User does not exist:', username)
        except Onlineuser.DoesNotExist:
            # Handle the case when the Onlineuser record does not exist for the user
            print('Onlineuser record does not exist for User:', username)


    def websocket_disconnect(self,event):
        async_to_sync(self.channel_layer.group_discard)(self.room_group_name,self.channel_name)
        print('Websocket status has been disconnected...')
        raise StopConsumer()
