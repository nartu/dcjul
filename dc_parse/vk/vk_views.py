from django.shortcuts import render, redirect
import os
import requests
from dc_parse.utils import write_json, build_uri
from dc_parse.utils import get_vk_cookies, vk_method
from dc_parse.utils import vk_json_image_url, vk_json_psql_time
from dc_parse.utils import put_tags_to_db
from django.contrib.sessions.models import Session
from dc_main.models import Media, Tag, TagMediaBond
from dc_parse.models import MediaVkPhoto, MediaVkPhotoThumbnail
from django.db import IntegrityError
from dc_parse.vk.vk_utils import vk_put_photos_to_db
from dc_parse.vk.vk_forms import ParseForm

def vk_get_photo_all(request):
    debug = {}
    if request.method == "POST":
        post = request.POST.copy()
        vk_token,vk_user = get_vk_cookies(request)
        method_name = 'photos.getAll'
        parameters = {
            'count': post.get('count'),
            'photo_sizes': 1,
            'extended': 1,
            'offset': post.get('offset')
        }
        form = ParseForm(post)
        tags = []
        tags_existed = post.getlist('tags_existed')
        tags_new = list(filter(lambda x: len(x)>0, list(map(str.strip, post.get('tags_new').split(',')))))
        debug['ar'] = (tags_existed,tags_new,type(tags_new))
        for tag_pk in tags_existed:
            tags += [Tag.objects.get(pk=int(tag_pk)).name]
        for tag_name in tags_new:
            if tag_name not in tags:
                tags += [tag_name]
        debug['result'] = tags
        content = vk_method(method_name,vk_token,parameters)
        resume = vk_put_photos_to_db(content,tags)
    else:
        form = ParseForm(dict(count=12,offset=5))
    return render(request,'vk_get_photo_all.html',{
            'form': form,
            'debug': debug
            })
    #     try:
    #         tags = request.GET.get('tags').split(',')
    #     except AttributeError:
    #         tags = ''
    #     content = vk_method(method_name,vk_token,parameters)
    #
    #     resume = vk_put_photos_to_db(content,tags)
    #
    #     return render(request,'vk_get_photo_album.html',{
    #         # 'content': content,
    #         'imgs': content['items'],
    #         'tags': tags,
    #         'resume': resume
    #         })



def vk_get_photo_album(request,album):
    vk_token,vk_user = get_vk_cookies(request)
    method_name = 'photos.get'
    parameters = {
        'album_id': album,  # 199663597
        'count': 4,
        'photo_sizes': 1,
        'extended': 1,
        'offset': 30,
        # 'photo_ids': 456239414
    }
    try:
        tags = request.GET.get('tags').split(',')
    except AttributeError:
        tags = ''
    content = vk_method(method_name,vk_token,parameters)

    resume = vk_put_photos_to_db(content,tags)

    return render(request,'vk_get_photo_album.html',{
        # 'content': content,
        'imgs': content['items'],
        'album': album,
        'tags': tags,
        'resume': resume
        })