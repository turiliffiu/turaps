from django import forms
from .models import Adpr, Scan
from django.forms import BaseModelFormSet




# creating a form
class MyModelFormSet(BaseModelFormSet):

    def add_fields(self, form, index):
        super().add_fields(form, index)
        form.fields['DELETE'].label = ''


class AdprForm(forms.ModelForm):
 
    # create meta class
    class Meta:
        # specify model to be used
        model = Adpr
 
        # specify fields to be used
        fields = [
            "id",
            "cella",
            "bb",
            "seq",
            "rusref",
            #"rdbubl",
            "rutype",
            "layer",
            "mxmod",
            "mimo",
            "tma",
            "ret",
            "utente",
        ]

class ScanForm(forms.ModelForm):
 
    # create meta class
    class Meta:
        # specify model to be used
        model = Scan
 
        # specify fields to be used
        fields = [
            "id",
            "bb",
            "radio",
            "seq",
            "port",
            "type",
            "unique_id",
            "product_number",
            "freq1tma",
            "utente",
        ]


