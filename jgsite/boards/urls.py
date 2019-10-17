from django.urls import path

from . import views

app_name = 'boards'
urlpatterns = [
    path('', views.home, name='home'),
    path('<int:board_id>/topics/', views.board_topics, name='board_topics'),
    path('<int:board_id>/topics/new/', views.new_topic, name='new_topic'),
    path('<int:board_id>/topic/<int:topic_id>/edit/', views.edit_topic, name='edit_topic'),
    path('<int:board_id>/topic/<int:topic_id>/posts/', views.topic_posts, name='topic_posts'),
    path('<int:board_id>/topic/<int:topic_id>/reply/', views.reply_topic, name='reply_topic'),
    
]