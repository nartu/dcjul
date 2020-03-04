from django.shortcuts import render
from .models import Tag, Media, TagMediaBond

def index(request):
    return render(request,'index.html',{})

def tags(request):
    return render(request,'tags.html',{})

def tag_list(request):
    tags = Tag.objects.order_by('pk')
    content = dict()
    print(tags)
    for tag in tags:
        content[tag.pk] = []
        media_ids = TagMediaBond.objects.filter(tag_id=tag.id)
        # content[tag.pk] = media_ids
        for media in media_ids:
            content[tag.pk] += Media.objects.filter(pk=media.pk)
    return render(request,'tag_list.html',{'tags': tags, 'content': content})
