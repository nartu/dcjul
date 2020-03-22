from django.shortcuts import render, redirect
from urllib.parse import urlencode, urlparse
from dc.settings import BASE_DIR
import os
import requests
import json
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

def vk_connect(request):
        code = request.GET.get('code')
        this_uri = request.build_absolute_uri()
        if code:    # second step auth
            url_data = {
            'client_id': 3410588,
            'client_secret': '0ijwqFsfD8NiTuSafIKH',
            'redirect_uri': build_uri(this_uri),
            'code': code}
            # url = build_uri('https://oauth.vk.com/access_token',url_query=url_data)
            # response = requests.get(url)
            response = requests.post('https://oauth.vk.com/access_token',data=url_data)
            rj = response.json()
            write_json(response.json(),'auth3.json')
            if rj.get('error'):
                return render(request,'vk_connect_test.html',{
                'step': 2,
                'status': 'fail',
                'error': rj['error'],
                'error_description': rj['error_description']})
            # if success set COOKIES
            request.session.set_test_cookie()
            if request.session.test_cookie_worked():
                request.session.delete_test_cookie()
                request.session['vk_auth_access_token'] = rj['access_token']
                request.session['vk_auth_expires_in'] = rj['expires_in']
                request.session['vk_auth_user_id'] = rj['user_id']
            else:
                pass
            return redirect('dc_parse:vk_connect_test')
        else:   # first step auth
            url_data = {
                'client_id': 3410588,
                'display': 'popup',
                'redirect_uri': build_uri(this_uri),
                'scope': 'photos',
                'response_type': 'code',
                'v': '5.103'}
            url = build_uri('https://oauth.vk.com/authorize',url_query=url_data)
            # If errors
            response = requests.get(url)
            try:
                rj = response.json()
                if rj['error']:
                    return render(request,'vk_connect_test.html',{
                    'step': 1,
                    'status': 'fail',
                    'error': rj['error'],
                    'error_description': rj['error_description']+'\n'+url
                    })
            except:   # No errors
                return redirect(url)

def vk_connect_test(request):
    step = 3
    error = None
    error_description = None
    content = ''
    cookies = request.COOKIES
    try:
        session_raw = Session.objects.get(pk=cookies['sessionid'])
        session = session_raw.get_decoded()
        status = 'success'
        # Test VK API
        vk_token = session['vk_auth_access_token']
        vk_user = session['vk_auth_user_id']
        # https://api.vk.com/method/users.get
        # ?user_ids=210700286&fields=bdate&access_token=&v=5.103
        method_name = 'users.get'
        parameters = {
            'user_ids': vk_user,
            'fields': 'bdate',
            'access_token': vk_token,
            'v': '5.103'
        }
        url = build_uri('https://api.vk.com/method/'+method_name,parameters)
        response = requests.post(os.path.join('https://api.vk.com/method',method_name)
            ,data=parameters)
        rj = response.json()
        content = rj['response'][0]
        # write_json(response.json(),'ans1.json')
    except KeyError:
        raise KeyError
        session = 'Unknown session'
        status = 'fail'
    except Exception:
        raise Exception
        session = 'WTF?'
        status = 'Unknown'
    return render(request,'vk_connect_test.html',{
        'content': content,
        'step': step,
        'session': 'session',
        'status': status,
        'error': error,
        'error_description': error_description})

def cookie_test(request):
    request.session.set_test_cookie()
    request.session["fav_color"] = "blue"
    request.session["xz"] = "test_sting"
    cookies = request.COOKIES
    test = request.session.test_cookie_worked()
    s = Session.objects.get(pk=cookies['sessionid'])
    test = (s.session_data, s.expire_date)
    test = s.get_decoded()
    return render(request,'cookie_test.html',{'cookies': cookies, 'test': test})
