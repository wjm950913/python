from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'/index$', views.indexview),
    url(r'/publish$', views.topic_publish),
    url(r'/send$', views.comment_send),
]
