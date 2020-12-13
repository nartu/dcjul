from django.shortcuts import render, redirect
from dc_parse.edit.test_forms import TestForm, MediaTestForm
from dc_parse.edit.forms import EditMediaForm
from dc_main.models import Media, Tag, TagMediaBond
from dc_parse.utils import put_tags_to_db, prepare_tags

def test(request):
    debug=request.POST
    data = {'count': 7,'test_checkboxes': [1,3]}
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

    form_populate = {
        'description_me':media.description_me,
        'description_auto':media.description_auto,
        'tags_existed':tags_existed
        }
    form = EditMediaForm(form_populate)

    debug = {'tags': tags_existed}
    debug = {'post': request.POST}

    # Add to db
    if request.method == "POST":
        post = request.POST
        tags = prepare_tags(post.getlist('tags_existed'),post.get('tags_new'))
        resume_tags = put_tags_to_db(tags, media)
        media.description_me = post.get('description_me')
        media.save()
        debug = {'tags': tags_existed, 'tags_resume':resume_tags}
        return redirect('dc_parse:edit_media',media_pk=media_pk)
    else:
        return render(request,'edit/edit_media.html',{
                'form': form,
                'media': media,
                'debug': debug
                })
