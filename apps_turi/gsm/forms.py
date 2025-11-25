from django import forms
from .models import ScriptGsm


class ScriptGsmModelForm(forms.ModelForm):
    class Meta:
        model = ScriptGsm
        fields = ["bb", "script"]
        widgets = {"script": forms.Textarea(attrs={'cols': 120, 'rows': 10}),}
        labels = {"script": "", "bb": ""}

