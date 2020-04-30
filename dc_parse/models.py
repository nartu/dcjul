from django.db import models
# from dc_main.models import Media

class MediaVkPhoto(models.Model):
    """
    media_id (dc_main.models.Media),
    photo, album, owner, post (vk_id),
    comments, tags [boolean]
    """
    media = models.OneToOneField('dc_main.Media',
        on_delete=models.CASCADE, primary_key=True) #media_id in db
    photo = models.IntegerField(unique=True)
    album = models.IntegerField()
    owner = models.IntegerField()
    post = models.IntegerField(blank=True,null=True)
    comments = models.BooleanField(blank=True)
    tags = models.BooleanField(blank=True)

class MediaVkPhotoThumbnail(models.Model):
    """
    media_id (dc_main.models.Media),
    s, m, x [url]
    """
    media = models.OneToOneField('dc_main.Media',
        on_delete=models.CASCADE, primary_key=True) #media_id in db
    s = models.URLField(max_length=255)
    m = models.URLField(max_length=255, blank=True)
    x = models.URLField(max_length=255, blank=True)
