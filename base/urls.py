from django.urls import path, include
from . import views
 
urlpatterns=[
    path('',views.home,name='home') ,
    path('avaliable/',views.avaliable,name='avaliable'),
    path('login/',views.loginUser,name='login'),
    path('logout/',views.logoutUser, name='logout'),
    path('addwork/',views.addwork, name='addwork'),
    path('viewwork/',views.viewwork, name='viewwork'),
    path('modifywork/<str:work_id>',views.modifywork, name='modifywork'),
    path('assignwork',views.assign_work_view,name='assignwork'),
    path('assign_work/<str:work_id>',views.assign_work,name='assign_work'),
 ]