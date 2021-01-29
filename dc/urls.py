"""dc URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('v1/', include('dc_main.urls_v1',namespace='dc_v1')),
    path('admin/parse/', include('dc_parse.urls',namespace='dc_parse')),
    path('gallery/', include('dc_gallery.urls',namespace='dc_gallery')),
    path('', include('dc_main.urls',namespace='dc_main')),
    path('api/', include('dc_api.urls',namespace='dc_api')),
]
