"""untitled4 URL Configuration

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

#和views这个py文件一同写，函数和模块关联使用,
from django.contrib import admin
from django.urls import path
#from.views import login,class_list,delete_class,add_class,edit_class,student_list,delete_student,add_student
#from . import views这个可以使上方的都简略，只需要在path路径里加views.
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/',views.login),
    #要跳转至函数class_list的html，后缀加/class_list/，函数对应路径
    #班级表单
    path('class_list/',views.class_list),
    path('delete_class/',views.delete_class),
    path('add_class/',views.add_class),
    path('edit_class/',views.edit_class),
    #学生表单
    path('student_list/',views.student_list),
    path('delete_student/',views.delete_student),
    path('add_student/',views.add_student),
    path('edit_student/',views.edit_student),
    #老师表单
    path('teacher_list/', views.teacher_list),
    path('delete_teacher/', views.delete_teacher),
    path('add/', views.add_teacher,name='add_teacher'),
    path('edit/', views.edit_teacher,name='edit_teacher'),
    path('search_teacher/', views.search_teacher),
    path('zdenglu/', views.zdenglu),
]



