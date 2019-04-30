from django.urls import path

from . import views

app_name = 'boards'
urlpatterns = [
    path('', views.home, name='home'),
    path('<int:board_id>/topics/', views.board_topics, name='board_topics'),
    path('<int:board_id>/topics/new/', views.new_topic, name='new_topic'),
    
]