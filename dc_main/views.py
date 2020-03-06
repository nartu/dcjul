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
        content[tag.pk] = {'tag': tag, 'media': []}
        media_ids = TagMediaBond.objects.filter(tag_id=tag.pk)
        for media in media_ids:
            content[tag.pk]['media'] += Media.objects.filter(pk=media.pk)
    return render(request,'tag_list.html',{'tags': tags, 'content': content})
