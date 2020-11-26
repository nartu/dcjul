from django.shortcuts import render, get_object_or_404, redirect
from dc_main.models import Tag, Media, TagMediaBond
from dc_parse.models import MediaVkPhotoThumbnail
from django.core.paginator import Paginator

# Static pages

def index(request):
    return render(request,'dc_design/index.html',{
        })

def about(request):
    return render(request,'dc_design/about.html',{
        })

def contact(request):
    return render(request,'dc_design/contact.html',{
        })


# Gallery (media agregator)

def gallery(request):
    return redirect('dc_gallery:gallery_tag', tag_pk=1)
    # return render(request,'dc_design/gallery.html',{
    #     # 'form': form,
    #     # 'debug': debug
    #     })

def gallery_tag(request,tag_pk):
    tags = Tag.objects.order_by('pk')
    tag_target = get_object_or_404(Tag,pk=tag_pk)
    media_list = list()
    media_ids = TagMediaBond.objects.filter(tag_id=tag_target.pk)
    for media in media_ids:
        media_list += Media.objects.filter(pk=media.pk)
    # pages, objects per page
    media_paginator = Paginator(media_list,4)
    page = request.GET.get('page')
    media_list_page = media_paginator.get_page(page)
    return render(request,'dc_design/gallery.html',{
        'tags': tags,
        'tag_target': tag_target,
        'media_list': media_list_page
    })

def media_detail(request,media_pk):
    """ Media detail by ID or message 'not exits' """
    # media = Media.objects.filter(pk=pk)
    media = get_object_or_404(Media,pk=media_pk)
    if MediaVkPhotoThumbnail.objects.filter(media_id=media_pk):
        media_thumbnail =  MediaVkPhotoThumbnail.objects.get(media_id=media_pk).x
    else:
        media_thumbnail =  None
    return render(request,'dc_design/media_detail.html',{
    'media_thumbnail': media_thumbnail,
    'media': media})
