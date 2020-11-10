from django.shortcuts import render, redirect
from dc_parse.utils import write_json, build_uri
from dc_parse.utils import get_vk_cookies, vk_method

def vk_utils_photo_info(request):
    vk_token,vk_user = get_vk_cookies(request)
    method_name = 'photos.get'
    parameters = {
        'album_id': 199663597,  # 199663597
        'count': 1,
        'photo_sizes': 1,
        'extended': 1,
        'offset': 8,
        # 'photo_ids': 456239414
    }
    content = vk_method(method_name,vk_token,parameters)
    # write_json(content,'photo2.json')
    sizes = content['items'][0]['sizes']
    id = content['items'][0]['id']
    album = content['items'][0]['album_id']
    return render(request,'utils/vk_utils_photo_info.html',{
        # 'content': content,
        'sizes': sizes,
        'id': id,
        'album': album
        })
