from django.urls import path
from . import views

app_name = 'crud'

urlpatterns = [
    path('', views.index, name='index' ),
    path('create/', views.create, name='create' ),
    path('add_client/', views.add_client, name='add_client' ),
    path('delete/<id>/', views.delete, name='delete' ),
    path('edit/<id>/', views.edit, name='edit' ),
    path('update/<id>/', views.update, name='update' ),
]
