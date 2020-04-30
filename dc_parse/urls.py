from django.urls import path
from . import views, subviews

app_name = 'dc_parse'
urlpatterns = [
    # path('vk/test', views.vk_test, name='vk_test'),
    # path('cookies',views.cookie_test, name='cookie_test'),
    path('vk/connect/', views.vk_connect, name='vk_connect'),
    path('vk/connect/test/', views.vk_connect_test, name='vk_connect_test'),
    path('vk/get/photo/<album>/', views.vk_get_photo_album, name='vk_get_photo_album'),
    path('vk/utils/photoinfo', subviews.vk_utils_photo_info, name='vk_utils_photo_info')
]
