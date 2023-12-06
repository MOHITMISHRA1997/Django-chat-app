from django.contrib import admin
from .models import Chat,Group,Onlineuser,Userprofile

# Register your models here.

admin.site.register(Chat)
admin.site.register(Group)
admin.site.register(Onlineuser)
admin.site.register(Userprofile)
