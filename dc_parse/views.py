from django.shortcuts import render, redirect
from django.urls import reverse

def link_all(request):
    """ all links admin/parse """
    if not request.user.is_superuser:
        return redirect('%s?next=%s' % (reverse('dc_parse:admin_auth'), request.path))

    return render(request,'link_all.html',{})
