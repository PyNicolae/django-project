from django.contrib import admin
from django.urls import path,include
from filetransfer import views
from django.urls import re_path
from django.views.static import serve
from django.conf import settings

urlpatterns = [
    path('',views.home, name="home"),
    path('register', views.register, name="register"),
    path('signin', views.signin, name="signin"),
    path('signout', views.signout, name="signout"),
    path('upload', views.upload_file, name="upload"),
    path('aboutus', views.aboutus, name="aboutus"),
    path('download/<file_name>/', views.download_file, name="download"),
    path('download/', views.download_page, name="download_page")
]