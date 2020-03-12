from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('tags', views.tags, name='tags'),
    path('tag/list', views.tag_list, name='tag_list'),
    path('tag/<int:pk>', views.tag_detail, name='tag_detail'),
    path('media/<int:pk>', views.media_detail, name='media_detail'),
]
