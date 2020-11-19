from django import forms
from dc_main.models import Tag

class ParseForm(forms.Form):
    count = forms.IntegerField(required=False,min_value=1)
    offset = forms.IntegerField(required=False,min_value=0)
    tags_new = forms.CharField(widget=forms.Textarea({'rows': 2}),required=False)

    tags_existed_choises = []
    for tag in Tag.objects.all():
        tags_existed_choises += [(tag.pk, tag.name)]
    tags_existed = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple(),
        choices=tags_existed_choises,required=False)


    # tag_existed_choises = [('one',1),('two',2)]
    # tag_existed = forms.ChoiceField(widget=forms.CheckboxSelectMultiple({'checked':'checked'}),choices=tag_existed_choises)
    # test = forms.ChoiceField(widget=forms.CheckboxInput,required=True)
