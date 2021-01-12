from django.db import models
from django.utils import timezone
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

class StatUpload(models.Model):
    """
    Statistica of uploads in bd
    Time (when upload)
    Num (photos per action)
    Action (add, edit, delete, update [media/tags], bind [media to tag], bind_delete)
    Method (page: all, album-N, album-all, edit-media)
    """
    time = models.DateTimeField(
            default=timezone.now)
    num = models.IntegerField()
    action = models.CharField(max_length=20)
    method = models.CharField(max_length=20)
    media = models.ForeignKey('dc_main.Media',on_delete=models.CASCADE,blank=True,null=True)

    def __str__(self):
        return f"{self.num} {self.action} in Media_{self.media.id} by {self.method}"
