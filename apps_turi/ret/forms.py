from django import forms
from django.forms import BaseModelFormSet, modelformset_factory
from .models import ScriptRet, SwapMatrix, CellRet



class MyModelFormSet(BaseModelFormSet):

    def add_fields(self, form, index):
        super().add_fields(form, index)
        form.fields['DELETE'].label = ''

class ScriptRetModelForm(forms.ModelForm):
    class Meta:
        model = ScriptRet
        fields = ["bb1", "script1", "bb2", "script2"]
        widgets = {"script1": forms.Textarea(attrs={'cols': 120, 'rows': 10}), "script2": forms.Textarea(attrs={'cols': 120, 'rows': 10}),}
        labels = {"script1": "", "script2": "", "bb1": "", "bb2": ""}

class ScriptRetModelForm1(forms.ModelForm):
    class Meta:
        model = ScriptRet
        fields = ["bb1", "script1"]
        widgets = {"script1": forms.Textarea(attrs={'cols': 120, 'rows': 10})}
        labels = {"script1": "", "bb1": ""}
        
class SwapMatrixForm(forms.ModelForm):
    class Meta:
        model = SwapMatrix
        fields = [ "sito", "sttr", "seceq", "banda", "serial", "radctrl", "porta", "prog", "eltlt", "usrlbl", "tmplt"]    

CellRetFormSet = modelformset_factory(CellRet, fields=('id', 'master', 'bb', 'cell', 'seq', 'radio', 'mimo', 'tilt', 'utente', 'ordine'))