from django.shortcuts import render, get_object_or_404
from .models import Tag, Media, TagMediaBond
from django.core.paginator import Paginator
# from django.shortcuts import redirect

def index(request):
    return render(request,'index.html',{})

def tags(request):
    return render(request,'tags.html',{})

def tag_list(request):
    tags = Tag.objects.order_by('pk')
    tags_paginator = Paginator(tags,1)
    page = request.GET.get('page')
    tags_page = tags_paginator.get_page(page)
    content = dict()
    for tag in tags_page:
        content[tag.pk] = {'tag': tag, 'media': []}
        media_ids = TagMediaBond.objects.filter(tag_id=tag.pk)
        for media in media_ids:
            content[tag.pk]['media'] += Media.objects.filter(pk=media.pk)
    return render(request,'tag_list.html',{'tags': tags, 'content': content})

def tag_detail(request):
    """ All about tag: created, language, media """
    pass

def tag_link(request,pk):
    tags = Tag.objects.order_by('pk')
    tag_target = get_object_or_404(Tag,pk=pk)
    media_list = list()
    media_ids = TagMediaBond.objects.filter(tag_id=tag_target.pk)
    for media in media_ids:
        media_list += Media.objects.filter(pk=media.pk)
    return render(request,'tag_link.html',{
        'tags': tags,
        'tag_target': tag_target,
        'media_list': media_list
    })

def media_detail(request,pk):
    """ Media detail ID """
    # media = Media.objects.filter(pk=pk)
    media = get_object_or_404(Media,pk=pk)
    return render(request,'media_detail.html',{'media': media})

def media_list(request):
    """ All medias """
    media_list = Media.objects.all()
    return render(request,'media_list.html',{'media_list': media_list})
