from django import forms
from .models import ScriptTma, Tma, DeMatrix
from django.forms import BaseModelFormSet

class MyModelFormSet(BaseModelFormSet):
    # Estende la classe BaseModelFormSet per personalizzare i campi del formset
    def add_fields(self, form, index):
        super().add_fields(form, index)
        form.fields['DELETE'].label = ''  # Rimuove l'etichetta dal campo 'DELETE'

class ScriptTmaModelForm(forms.ModelForm):
    class Meta:
        model = ScriptTma
        fields = ["bb1", "script1", "bb2", "script2"]
        widgets = {"script1": forms.Textarea(attrs={'cols': 120, 'rows': 10}), "script2": forms.Textarea(attrs={'cols': 120, 'rows': 10}),}
        labels = {"script1": "", "script2": "", "bb1": "", "bb2": ""}

class ScriptTmaModelForm1(forms.ModelForm):
    class Meta:
        model = ScriptTma
        fields = ["bb1", "script1"]
        widgets = {"script1": forms.Textarea(attrs={'cols': 120, 'rows': 10})}
        labels = {"script1": "", "bb1": ""}

class Script1TmaModelForm(forms.ModelForm):
    class Meta:
        model = ScriptTma
        fields = ["sito", "script1", "script2", "bb1", "bb2"]
        widgets = {"script1": forms.Textarea(attrs={'cols': 120, 'rows': 10}), "script2": forms.Textarea(attrs={'cols': 120, 'rows': 10}),}
        labels = {"script1": "Script1", "script2": "Script2"}

class TmaForm(forms.ModelForm):
    # create meta class
    class Meta:
        # specify model to be used
        model = Tma
        # specify fields to be used
        fields = [
            "cella",
            "bb",
            "seq",
            "radio",
            "rutype",
            "layer",
            "mimo",
            "mimop",
            "port",
            "serial1",
            "serial2",
            "dlAttenuation",
            "dlTrafficDelay",
            "ulTrafficDelay",
            "tmatype",
            "subunit",
            "codtmpl",
            "utente",
            "tsua",
            "tsub",
            "laye2"
        ]        

class DeMatrixForm(forms.ModelForm):

    class Meta:

        model = DeMatrix

        fields = [
            "tmatype",
            "subunit",
            "layer",
            "seqsref",
            "cellafr",
            "cellaly",
            "mimo44",
            "mimo44p",
            "tsua",
            "tsub",
            "laye2",
            "cdtmpl"
        ]  
        