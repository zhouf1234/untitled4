"""Django01 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.urls import path
from .views import login,class_list,delete_class,add_class,edit_class


urlpatterns = [
    path('login/',login),
    path('class_list/',class_list),
    path('delete_class/',delete_class),
    path('add_class/',add_class),
    path('edit_class/',edit_class)
    # path('admin/', admin.site.urls),
]
