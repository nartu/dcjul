from django.urls import path
from dc_gallery import views as views_gallery

app_name = 'dc_main'
urlpatterns = [
    path('', views_gallery.index, name='index'),
    path('about', views_gallery.about, name='about'),
    path('contact', views_gallery.contact, name='contact'),
]
