from django.shortcuts import render, get_object_or_404, redirect
from dc_main.models import Tag, Media, TagMediaBond
from django.core.paginator import Paginator


def gallery(request):
    return render(request,'gallery.html',{
        # 'form': form,
        # 'debug': debug
        })

def gallery_tag(request,tag_pk):
    tags = Tag.objects.order_by('pk')
    tag_target = get_object_or_404(Tag,pk=tag_pk)
    media_list = list()
    media_ids = TagMediaBond.objects.filter(tag_id=tag_target.pk)
    for media in media_ids:
        media_list += Media.objects.filter(pk=media.pk)
    return render(request,'gallery.html',{
        'tags': tags,
        'tag_target': tag_target,
        'media_list': media_list
    })
