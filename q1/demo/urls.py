from django.urls import path
from . import views

app_name = 'code'

urlpatterns = [
    path('home/', views.index, name='index'),
    path('home/p/', views.post_index, name='post_index'),
]