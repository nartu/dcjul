from django.shortcuts import render, get_object_or_404
# from dc.settings import STATIC_ROOT as sr
from django.conf import settings as s

def test(request):
    return render(request,'test.html',{'static_root': s.STATIC_ROOT})
