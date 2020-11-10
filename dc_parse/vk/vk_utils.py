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


def vk_put_photos_to_db(json_answer,tags=''):
    """ put medias to db from json_answer,
        json_answer - answer['response'],
        return resume: media new, media existed, vk_photo_info_add, vk_thumbnail_add"""
    resume = {  'media_new': 0,
                'media_existed': 0,
                'vk_photo_info_add': 0,
                'vk_thumbnail_add': 0,
                'tag_new': 0,
                'tag_existed': 0,
                'tag_bonds': 0
                }
    content = json_answer
    # write_json(content,'photo.json')
    # sizes = content['items'][0]['sizes']
    for img in content['items']:
        # insert in psql, url - unique
        # dc_main.models.Media
        img_url = vk_json_image_url(img,include_thumbnail=True)
        try:
            media_new = Media.objects.create(
                type = 'image',
                source = 'vk',
                url = img_url['src'],
                url_thumbnail = img_url['thumbnail']['q'] if 'q' in img_url['thumbnail'] else '',
                description_auto = img['text'],
                created_date = vk_json_psql_time(img)
            )
            resume['media_new'] += 1
        except IntegrityError:  # db error, exist url unique
            media_new = Media.objects.get(url=img_url['src'])
            resume['media_existed'] += 1
        except Exception as e:
            raise e
        # dc_main.models.Tag TagMediaBond
        resume_tags = put_tags_to_db(tags,media_new)
        if(resume['tag_new']==0 and resume['tag_existed']==0):
            resume['tag_new'] += resume_tags['tag_new']
            resume['tag_existed'] += resume_tags['tag_existed']
        resume['tag_bonds'] += resume_tags['tag_bonds']

        # dc_parse.models.MediaVkPhoto
        if(not MediaVkPhoto.objects.filter(media=media_new).exists()):
            MediaVkPhoto.objects.create(
                media = media_new,
                photo = img['id'],
                album = img['album_id'],
                owner = img['owner_id'],
                post = img.get('post_id'),
                comments = bool(img['comments']['count']),
                tags = bool(img['tags']['count'])
            )
            resume['vk_photo_info_add'] += 1
        # dc_parse.models.MediaVkPhotoThumbnail
        if(not MediaVkPhotoThumbnail.objects.filter(media=media_new).exists()):
            MediaVkPhotoThumbnail.objects.create(
                media = media_new,
                s = img_url['thumbnail']['s'],
                m = img_url['thumbnail']['m'] if 'm' in img_url['thumbnail'] else '',
                x = img_url['thumbnail']['x'] if 'x' in img_url['thumbnail'] else ''
            )
            resume['vk_thumbnail_add'] += 1
    return resume
