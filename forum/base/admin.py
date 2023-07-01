from django.contrib import admin
from base.models import Room, Topic, Message, Feedback, User
# Register your models here.

admin.site.register(User)
admin.site.register(Room)
admin.site.register(Topic)
admin.site.register(Message)
admin.site.register(Feedback)