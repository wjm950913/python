from django.conf.urls import url

from user import views

urlpatterns = [
    url(r'^/login$', views.Login.as_view()),
    url(r'^/register$', views.Register.as_view()),
    url(r'^/myact$', views.Myact.as_view()),
    url(r'^/mygoods$', views.Mygoods.as_view()),
    url(r'^/myorder$', views.Myorder.as_view()),
    url(r'^/myreleases$', views.Myrelease.as_view()),
    url(r'^/news$', views.News.as_view()),
    url(r'^/personal$', views.Personal.as_view()),
]
