from django.urls import path, include
from . import views
 
urlpatterns=[
    path('',views.home,name='home') ,
    path('myworks/',views.myworks,name='myworks'),
    path('allemployees/',views.allemployees,name='allemployees'),
    path('avaliable/',views.avaliable,name='avaliable'),
    path('login/',views.loginUser,name='login'),
    path('logout/',views.logoutUser, name='logout'),
    path('addwork/',views.addwork, name='addwork'),
    path('viewwork/',views.viewwork, name='viewwork'),
    path('viewwork/<str:pk>',views.viewspecificwork, name='viewspecificwork'),
    path('modifywork/<str:work_id>',views.modifywork, name='modifywork'),
    path('assignwork',views.assign_work_view,name='assignwork'),
    path('assign_work/<str:work_id>',views.assign_work,name='assign_work'),
    path('update_presence/', views.update_presence, name='update_presence'),
    path('mark_work_completed/',views.mark_work_completed,name='mark_work_completed')
 ]