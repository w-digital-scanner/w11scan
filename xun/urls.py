"""xun URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,re_path
from app import views

urlpatterns = [
    # path(r'admin/', admin.site.urls),
    path(r'filter',views.search,name = "search"),
    path(r'task',views.task),
    path(r'plugin',views.plugin),
    path(r'plugin/<str:slug>',views.plugin),
    path(r'plugin_add',views.plugin_add),
    path(r'deleteplugin',views.plugin_del),
    path(r'analysis',views.analysis),
    path(r'config',views.config),
    path(r'login',views.login,name = "login"),
    path(r'',views.login),
    path(r'edit',views.edit,name='edit'),
    path(r'logout',views.logout),
    path(r'task_add',views.task_add),
    path(r'task_del',views.task_del),
    path(r'task/<str:slug>',views.detail,name="task_detail"),
    path(r'download/<str:slug>',views.download,name="download")
]
