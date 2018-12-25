"""HostApp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""

from django.conf.urls import url, include
from django.contrib import admin
from app01 import views

urlpatterns = [
    url(r'^business$', views.business),  # $符号是终止符，这样下边还可以在写business_add,也能匹配到
    url(r'^business_add$', views.business_add),
    url(r'^host$', views.host),  # $符号是终止符，这样下边还可以在写business_add,也能匹配到
    url(r'^host_del$', views.host_del.as_view()),
    url(r'^test_ajax$', views.test_ajax),
    url(r'^edit_ajax$', views.edit_ajax),
    url(r'^app$', views.app),
    url(r'^ajax_add_app$', views.ajax_add_app),
    url(r'^ajax_edit_app$', views.ajax_edit_app),
    url(r'^ajax_del_host_app$', views.ajax_del_host_app),
]