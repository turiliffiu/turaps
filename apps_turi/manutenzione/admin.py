from django.contrib import admin
from .models import TmplTma
# Register your models here.



class TmplTmaAdmin(admin.ModelAdmin):
    model = TmplTma
    list_display = ["cod", "tmpl"] 
    #list_display = ["titolo", "sezione_appartenenza", "autore_discussione"]
    #search_fields = ["titolo", "autore_discussione"]
    #list_filter = ["sezione_appartenenza", "data_creazione"]


admin.site.register(TmplTma, TmplTmaAdmin)    