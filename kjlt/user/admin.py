from django.contrib import admin

# Register your models here.
from forum.models import Topic, comment
from me.models import Goods
from user.models import *

admin.site.register(Order,)
admin.site.register(Msg,)
admin.site.register(Topic,)
admin.site.register(comment,)
admin.site.register(User,)
admin.site.register(Goods,)