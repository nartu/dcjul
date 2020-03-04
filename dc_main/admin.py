from django.contrib import admin
from .models import Tag, Media, TagMediaBond

admin.site.register(Tag)
admin.site.register(Media)
admin.site.register(TagMediaBond)
