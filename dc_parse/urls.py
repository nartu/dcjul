from django.urls import path
from .vk import vk_views, vk_subviews
from .views_connect import vk_connect
from .edit import views as edit_views
from . import views as common_views

app_name = 'dc_parse'
urlpatterns = [
    # Debug
    # path('vk/test', views.vk_test, name='vk_test'),
    # path('cookies',views.cookie_test, name='cookie_test'),
    # Auth
    path('login-admin', vk_connect.admin_auth, name='admin_auth'),
    # Connect
    path('vk/connect/', vk_connect.vk_connect, name='vk_connect'),
    path('vk/connect/test/', vk_connect.vk_connect_test, name='vk_connect_test'),
    path('vk/disconnect/', vk_connect.vk_disconnect, name='vk_disconnect'),
    # Parse for db
    path('vk/get/album/list', vk_views.vk_get_album_list, name='vk_get_album_list'),
    path('vk/get/photo/album-<album>/', vk_views.vk_get_photo_album, name='vk_get_photo_album'),
    path('vk/get/photo/fast/album-<album>/', vk_views.vk_get_photo_album_fast, name='vk_get_photo_album_fast'),
    path('vk/get/photo/all/', vk_views.vk_get_photo_all, name='vk_get_photo_all'),
    # Utils function (help)
    path('vk/utils/photoinfo', vk_subviews.vk_utils_photo_info, name='vk_utils_photo_info'),
    # Edit existed models
    path('edit/test', edit_views.test, name='edit_test'),
    path('edit/media/<int:media_pk>', edit_views.edit_media, name='edit_media'),
    # Links
    path('edit/media/list/ava', edit_views.edit_media_list_ava, name='edit_media_list_ava'),
    path('edit/media/list/table', edit_views.edit_media_list_table, name='edit_media_list_table'),
    path('', common_views.link_all, name='link_all')
]
