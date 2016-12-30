'''
Created on Oct 8, 2016

@author: chrisbradley
'''

from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
]
