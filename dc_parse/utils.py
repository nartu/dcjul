import os
import requests
import json
from urllib.parse import urlencode, urlparse
from dc.settings import BASE_DIR
from django.contrib.sessions.models import Session

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
    write_json(rj,'ans4.json')
    return content
