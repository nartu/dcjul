from django.db import models
from django.utils import timezone

class Tag(models.Model):
    """id, tag_name, created_date"""

    tag_name = models.CharField(max_length=90)
    created_date = models.DateTimeField(
            default=timezone.now)

    def __str__(self):
        return self.tag_name

class Media(models.Model):
    """
    id, type [image, video, text, audio], source [vk, youtube],
    url, url_thumbnail, description_auto, description_me,
    created_date, when_add_date, name (not required)
    """

    type = models.CharField(max_length=9)
    source  = models.CharField(max_length=12)
    url = models.URLField(max_length=255)
    url_thumbnail = models.URLField(max_length=255, blank=True)
    description_auto = models.TextField(blank=True)
    description_me = models.TextField(blank=True)
    created_date = models.DateTimeField()
    when_add_date = models.DateTimeField(
            default=timezone.now)
    name = models.CharField(max_length=255,blank=True)

class TagMediaBond(models.Model):
    """id_media, id_tag = unique"""

    media = models.ForeignKey('Media',on_delete=models.CASCADE)
    tag = models.ForeignKey('Tag',on_delete=models.CASCADE)

    class Meta:
        constraints = [
        models.constraints.UniqueConstraint(fields=['media', 'tag'],
         name='unique_bond')]

    def __str__(self):
        return "{}+{}".format(self.media.id,self.tag.tag_name)
