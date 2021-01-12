from django.shortcuts import render, get_object_or_404, redirect
from dc_main.models import Tag, Media, TagMediaBond
from dc_parse.models import MediaVkPhotoThumbnail
from django.core.paginator import Paginator
from django.db import IntegrityError

# Static pages

def index(request):
    return render(request,'dc_design/index.html',{
        'page_id': 'index'
        })

def about(request):
    return render(request,'dc_design/about.html',{
        'page_id': 'about'
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
        try:
            media_list += [Media.objects.get(pk=media.media_id)]
        except Media.DoesNotExist:
            media_list += Media.objects.filter(pk=4)
    # pages, objects per page
    media_paginator = Paginator(media_list,16)
    page = request.GET.get('page')
    media_list_page = media_paginator.get_page(page)
    # for p in range(media_paginator.num_pages):

    return render(request,'dc_design/gallery.html',{
        'tags': tags,
        'tag_target': tag_target,
        'media_list': media_list_page,
        'num_of_media': len(media_ids),
        'page_id': 'gallery'
    })

def media_detail(request,media_pk):
    """ Media detail by ID or message 'not exits' """
    # media = Media.objects.filter(pk=pk)
    media = get_object_or_404(Media,pk=media_pk)
    if MediaVkPhotoThumbnail.objects.filter(media_id=media_pk):
        media_thumbnail =  MediaVkPhotoThumbnail.objects.get(media_id=media_pk).x
    else:
        media_thumbnail =  None
    # array of tags instances of media
    tags = []
    tags_of_media = TagMediaBond.objects.filter(media=media_pk)
    for tmb in tags_of_media:
        tags += [tmb.tag]
    return render(request,'dc_design/media_detail.html',{
        'media_thumbnail': media_thumbnail,
        'media': media,
        'page_id': 'gallery',
        'tags': tags
    })
