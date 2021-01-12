from django import forms
from dc_main.models import Media

class TestForm(forms.Form):
    count = forms.IntegerField(required=False,min_value=0)
    d=[(1,'one'),(2,'two'),(3,'three')]
    test_checkboxes = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple(),
        choices=d,required=False)
    description_add = forms.CharField(widget=forms.Textarea({'rows': 4}),required=False)
    bool = forms.BooleanField(required=False)

class MediaTestForm(forms.ModelForm):
    class Meta:
        model = Media
        fields = '__all__'
