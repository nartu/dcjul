from django.shortcuts import render, redirect
import os
import requests
from dc_parse.utils import write_json, build_uri
from dc_parse.utils import get_vk_cookies, vk_method
from dc_parse.vk.vk_utils import vk_admin_auth
from django.contrib.sessions.models import Session
from django.contrib.auth.decorators import login_required, permission_required
from django.urls import reverse
from dc.settings import DEBUG
from dc.secret import get_vk_token

def admin_auth(request):
    """ request.user - current user, login for admin"""
    next = request.GET.get('next')
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % ('/admin/login/', next))
        # return redirect('/admin/login/')
    if not request.user.is_superuser:
        return redirect('/')
    # Put to every admin view
    # if not request.user.is_superuser:
    #     return redirect('%s?next=%s' % (reverse('dc_parse:admin_auth'), request.path))

def vk_connect(request):
    if not request.user.is_superuser:
        return redirect('%s?next=%s' % (reverse('dc_parse:admin_auth'), request.path))
    code = request.GET.get('code')
    this_uri = request.build_absolute_uri()
    if code:    # second step auth
        url_data = {
        'client_id': 3410588,
        'client_secret': get_vk_token(DEBUG),
        'redirect_uri': build_uri(this_uri),
        'code': code}
        # url = build_uri('https://oauth.vk.com/access_token',url_query=url_data)
        # response = requests.get(url)
        response = requests.post('https://oauth.vk.com/access_token',data=url_data)
        rj = response.json()
        write_json(response.json(),'auth10.json')
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
            'redirect_uri': build_uri(this_uri),    # '/' in the end
            'scope': 'photos',
            'response_type': 'code',
            'v': '5.103'}
        url = build_uri('https://oauth.vk.com/authorize',url_query=url_data)
        # If errors
        response = requests.get(url)
        try:
            rj = response.json()
            write_json(rj,'ans_er_1.json')
            if rj['error']:
                return render(request,'connect/vk_connect_test.html',{
                'step': 1,
                'status': 'fail',
                'error': rj['error'],
                'error_description': rj['error_description']+'\n'+url
                +'\n'+request.build_absolute_uri()
                })
        except:   # No errors
            return redirect(url)

def vk_connect_test(request):
    if not request.user.is_superuser:
        return redirect('%s?next=%s' % (reverse('dc_parse:admin_auth'), request.path))
    step = 3
    error = None
    error_description = None
    content = ''
    cookies = request.COOKIES
    session = ''
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
        # url = build_uri('https://api.vk.com/method/'+method_name,parameters)
        response = requests.post(os.path.join('https://api.vk.com/method',method_name)
            ,data=parameters)
        rj = response.json()
        content = rj['response'][0]
        # write_json(response.json(),'ans1.json')
    except KeyError:
        # raise KeyError
        session_raw = 'Unknown session'
        status = 'fail'
    except Exception:
        raise Exception
        session = 'WTF?'
        status = 'Unknown'
    return render(request,'connect/vk_connect_test.html',{
        'content': content,
        'step': step,
        'session': session,
        'status': status,
        'error': error,
        'error_description': error_description})

def vk_disconnect(request):
    if not request.user.is_superuser:
        return redirect('%s?next=%s' % (reverse('dc_parse:admin_auth'), request.path))
    step = 0
    error = None
    error_description = None
    content = ''
    cookies = request.COOKIES
    try:
        session_raw = Session.objects.get(pk=cookies['sessionid'])
        session = session_raw.get_decoded()
        status = 'session exists'
        # Test VK API
        try:
            # del session['vk_auth_access_token']
            # del session['vk_auth_user_id']
            # del session['vk_auth_expires_in']
            request.session.flush()
            status += ', del'
        except KeyError:
            status += ', vk api was not connect'
    # if session not exist
    except KeyError:
        # raise KeyError
        session_raw = 'Unknown session'
        status = 'fail'
    except Exception:
        raise Exception
        session = 'WTF?'
        status = 'Unknown'
    # return redirect('dc_parse:vk_connect_test')
    return render(request,'connect/vk_connect_test.html',{
        'content': content,
        'step': step,
        'session': session_raw,
        'status': status,
        'error': error,
        'error_description': error_description})
