from django.urls import path

from . import views

urlpatterns=[
    path('', views.home , name='home'),
    
    path('register/', views.register , name='register'),
    path('Login/', views.Login , name='Login'),
    path('upload_document/', views.upload_document, name='upload_document'),
     path('view_uploaded_files/', views.view_uploaded_files, name='view_uploaded_files'),
    path('LogOut/', views.LogOut , name='LogOut')
]