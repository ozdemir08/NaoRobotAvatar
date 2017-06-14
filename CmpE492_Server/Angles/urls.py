from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^postData$', views.postData, name='index'),
    url(r'^getData$', views.getData),
]