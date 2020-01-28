from django.urls import path
# from django.conf.urls import url
from . import views
app_name = 'my_notes_app'

urlpatterns = [
    path('', views.index, name='index'),
    path('index/', views.index, name='index'),
    path('topics/', views.topics, name='topics'),
    path('topics/<topic_id>/', views.topic, name='topic'),
    path('new_topic/', views.new_topic, name='new_topic'),
    path('new_entry/<topic_id>', views.new_entry, name='new_entry'),
    path('edit_entry/<entry_id>', views.edit_entry, name='edit_entry'),
    path('delete_entry/<entry_id>', views.delete_entry, name='delete_entry'),
    path('delete_topic/<topic_id>', views.delete_topic, name='delete_topic'),
    path('edit_topic/<topic_id>', views.edit_topic, name='edit_topic'),
]
