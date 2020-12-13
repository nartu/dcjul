from django import forms
from dc_main.models import Media, Tag, TagMediaBond

class EditMediaForm(forms.Form):
    """ edit description_auto, description_me, tags in Media insatnce """
    tags_new = forms.CharField(widget=forms.Textarea({'rows': 2}),required=False)

    tags_existed_choises = []
    for tag in Tag.objects.all():
        tags_existed_choises += [(tag.pk, tag.name)]
    tags_existed = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple(),
        choices=tags_existed_choises,required=False)

    description_auto = forms.CharField(widget=forms.Textarea({'rows': 4}),required=False)
    description_auto.label = "Description auto. Will not save!"

    description_me = forms.CharField(widget=forms.Textarea({'rows': 4}),required=False)
