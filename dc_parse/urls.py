from django.urls import path
from .vk import vk_views, vk_subviews
from .views_connect import vk_connect

app_name = 'dc_parse'
urlpatterns = [
    # Debug
    # path('vk/test', views.vk_test, name='vk_test'),
    # path('cookies',views.cookie_test, name='cookie_test'),
    # Connect
    path('vk/connect/', vk_connect.vk_connect, name='vk_connect'),
    path('vk/connect/test/', vk_connect.vk_connect_test, name='vk_connect_test'),
    path('vk/disconnect/', vk_connect.vk_disconnect, name='vk_disconnect'),
    # Parse for db
    path('vk/get/photo/<album>/', vk_views.vk_get_photo_album, name='vk_get_photo_album'),
    # Utils function (help)
    path('vk/utils/photoinfo', vk_subviews.vk_utils_photo_info, name='vk_utils_photo_info')
]
