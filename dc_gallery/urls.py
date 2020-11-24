from django.urls import path
from . import views


app_name = 'dc_gallery'
urlpatterns = [
    path('', views.gallery, name='gallery'),
    path('tag/<int:tag_pk>', views.gallery_tag, name='gallery_tag'),
    # change path later
    path('index', views.index, name='index'),
    path('about', views.about, name='about'),
    path('contact', views.contact, name='contact'),
]
