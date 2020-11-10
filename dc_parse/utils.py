import os
import requests
import json
from urllib.parse import urlencode, urlparse
from dc.settings import BASE_DIR
from django.contrib.sessions.models import Session
import datetime
from dc_main.models import Media, Tag, TagMediaBond
from django.db import IntegrityError

def write_json(data='',filename='answer.json'):
    save_dir = os.path.join(BASE_DIR,'dc_parse','debug','json')
    filename = os.path.join(save_dir,filename)
    with open(filename, 'w') as file:
        #write to file
        json.dump(data, file, indent=2,ensure_ascii=False)

def build_uri(url_src,url_query={}):
    url = urlparse(url_src)
    base = url.scheme + '://' + url.netloc + url.path
    if len(url_query)>0:
        query = '?' + urlencode(url_query, safe='/:?&=')
    else:
        query = ''
    url_result = base + query
    return url_result

def get_vk_cookies(request):
    try:
        cookies = request.COOKIES
        session_raw = Session.objects.get(pk=cookies['sessionid'])
        session = session_raw.get_decoded()
        vk_token = session['vk_auth_access_token']
        vk_user = session['vk_auth_user_id']
        return (vk_token,vk_user)
    except KeyError:
        return False

def vk_method(method_name,access_token,parameters={},v='5.103'):
    parameters_hard = {
        'access_token': access_token,
        'v': '5.103'
    }
    parameters.update(parameters_hard)
    # for get request
    # url = build_uri('https://api.vk.com/method/'+method_name,parameters)
    # requests.get(url)
    response = requests.post(os.path.join('https://api.vk.com/method',method_name)
        ,data=parameters)
    rj = response.json()
    if rj.get('error'):
        content = 'error' + '\n' + rj['error']['error_msg']
    else:
        content = rj['response']
    # write_json(rj,'ans4.json')
    return content

def vk_json_image_url(image,include_src=True,include_thumbnail=True):
# image url, src - z, thubnails - smx
# image from json answer ans['items'][n] n=0...ans['count']-1
    result = dict()
    thumbnail = dict()
    thumbnail_mask = list('smqx')
    src_mask = list('wzyxms')
    sizes_of_image = list()
    for size in image['sizes']:
        sizes_of_image += size['type']
    if(include_src):
        for t in src_mask:
            if t in sizes_of_image:
                i = sizes_of_image.index(t)
                src = image['sizes'][i]['url']
                break
        result['src'] = src
    if(include_thumbnail):
        for t in thumbnail_mask:
            if t in sizes_of_image:
                i = sizes_of_image.index(t)
                thumbnail[t] = image['sizes'][i]['url']
        result['thumbnail'] = thumbnail
    return result

def vk_json_psql_time(image):
# from unix to postgres standart timestamp
# image the same in vk_json_image_url
    date = datetime.datetime.fromtimestamp(image['date'])
    return date

def put_tags_to_db(tags, media):
    """ tags - array, media - dc_main.models.Media,
        to dc_main.models.Tag, TagMediaBond,
        return resume """
    resume = {
            'tag_new': 0,
            'tag_existed': 0,
            'tag_bonds': 0
            }
    for tag in tags:
        try:
            tag_obj = Tag.objects.get(name=tag)
            resume['tag_existed'] += 1
        except Tag.DoesNotExist:
            tag_obj = Tag.objects.create(name=tag)
            resume['tag_new'] += 1
        # except NameError:
        #     raise NameError
        except Exception as e:
            raise e
        try:
            TagMediaBond.objects.create(
                media = media,
                tag = tag_obj
            )
            resume['tag_bonds'] += 1
        except IntegrityError:  # if in db already (import django.db)
            pass

    return resume
