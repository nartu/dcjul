from django.shortcuts import render, redirect
from django.urls import reverse
from dc_parse.edit.test_forms import TestForm, MediaTestForm
from dc_parse.edit.forms import EditMediaForm
from dc_main.models import Media, Tag, TagMediaBond
from dc_parse.models import StatUpload
from dc_parse.utils import put_tags_to_db, prepare_tags
import time
from django.http import HttpResponse
from django.utils.cache import add_never_cache_headers
from django.views.decorators.cache import cache_page
from django.core.cache import cache
from django.db.models import Min

def test(request):
    debug=request.POST
    data = {'count': 7,'test_checkboxes': [1,3],'bool':True}
    media = Media.objects.get(pk=1)
    data.update({'description_add':media.description_auto})
    form = TestForm(data)
    # for save
    # form_media = MediaTestForm(request.POST,instance=media)
    return render(request,'edit/test.html',{
            'form': form,
            # 'form_media': form_media,
            'debug': debug
            })

@cache_page(0)
def edit_media(request,media_pk):
    """ put tags and description_me in Media instance """
    if not request.user.is_superuser:
        return redirect('%s?next=%s' % (reverse('dc_parse:admin_auth'), request.path))
    # Common data
    media = Media.objects.get(pk=media_pk)
    tags_existed = []
    tags_of_media = TagMediaBond.objects.filter(media=media_pk)
    for tmb in tags_of_media:
        tags_existed += [tmb.tag.pk]

    media_pk_next = Media.objects.filter(when_add_date__gt=media.when_add_date).aggregate(Min('pk'))['pk__min']

    form_populate = {
        'description_me':media.description_me,
        'description_auto':media.description_auto,
        'tags_existed':tags_existed,
        'redirect_next':True
        }

    form = EditMediaForm(form_populate)

    debug = {'media_next': media_pk_next}
    debug.update({'post': request.POST})
    debug.update({'tags_existed': tags_existed})
    # Add to db
    if request.method == "POST":
        post = request.POST
        tags = prepare_tags(post.getlist('tags_existed'),post.get('tags_new'))
        resume_tags = put_tags_to_db(tags, media)
        if media.description_me != post.get('description_me'):
            media.description_me = post.get('description_me')
            StatUpload.objects.create(
                num = 1,
                action = 'edit_description',
                method = 'edit-media',
                media = media
            )
        media.save()
        stat_action = {
        # 'create_media': 'media_new',
        'create_tags': 'tag_new',
        'bind': 'tag_bonds',
        'bind_delete': 'tag_bonds_del'}
        for act,act_res in stat_action.items():
            if resume_tags[act_res]>0:
                StatUpload.objects.create(
                    num = resume_tags[act_res],
                    action = act,
                    method = 'edit-media',
                    media = media
                )
        debug = {'tags_existed': tags_existed, 'tags': tags, 'tags_resume':resume_tags}
        time.sleep(2)
        # cache.clear()
        if(post.get('redirect_media_info')):
            return redirect('dc_gallery:media_detail',media_pk=media_pk)
        elif(post.get('redirect_next')):
            return redirect('dc_parse:edit_media',media_pk=media_pk_next)
        else:
            return redirect('dc_parse:edit_media',media_pk=media_pk)
    else:
        pass

    response = render(request,'edit/edit_media.html',{
            'form': form,
            'media': media,
            'debug': debug
            })
    # add_never_cache_headers(response)
    # response = render_to_response("template.html", {})
    # no-cache, no-store
    response['Cache-Control'] = 'no-store'
    return response
