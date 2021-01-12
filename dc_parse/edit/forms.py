from django import forms
from dc_main.models import Media, Tag, TagMediaBond
import time

class EditMediaForm(forms.Form):
    """ edit description_auto, description_me, tags in Media insatnce """
    tags_new = forms.CharField(widget=forms.Textarea({'rows': 2}),required=False)

    tags_existed = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple(),
        choices=[],required=False)

    description_auto = forms.CharField(widget=forms.Textarea({'rows': 4}),required=False)
    description_auto.label = "Description auto. Will not save!"

    description_me = forms.CharField(widget=forms.Textarea({'rows': 4}),required=False)

    redirect_next = forms.BooleanField(required=False)
    redirect_media_info  = forms.BooleanField(required=False)

    def __init__(self, *args, **kwargs):
        super(EditMediaForm, self).__init__(*args, **kwargs)

        tags_existed_choises = []
        for tag in Tag.objects.all():
            tags_existed_choises += [(tag.pk, tag.name)]

        self.fields['tags_existed'].choices = tags_existed_choises
        self.fields['tags_existed'].label = str(time.time())
