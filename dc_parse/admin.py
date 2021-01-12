from django.contrib import admin
from .models import MediaVkPhoto, MediaVkPhotoThumbnail
from .models import StatUpload

admin.site.register(MediaVkPhoto)
admin.site.register(MediaVkPhotoThumbnail)
admin.site.register(StatUpload)
