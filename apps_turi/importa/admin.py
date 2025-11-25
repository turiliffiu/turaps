from django.contrib import admin
from .models import Adpr, Scan, ValoriTma
# Register your models here.



class AdprModelAdmin(admin.ModelAdmin):
    model = Adpr
    list_display = ["cella", "bb", "seq", "rusref", "rutype", "layer", "mxmod", "mimo", "tma", "ret", "tilt", "atdl", "rtel", "sistema", "utente"] 
    #list_display = ["titolo", "sezione_appartenenza", "autore_discussione"]
    #search_fields = ["titolo", "autore_discussione"]
    #list_filter = ["sezione_appartenenza", "data_creazione"]

class ScanModelAdmin(admin.ModelAdmin):
    model = Scan
    list_display = ["bb", "radio", "seq", "port", "type", "unique_id", "product_number", "freq1tma", "utente"] 
    #list_display = ["titolo", "sezione_appartenenza", "autore_discussione"]
    #search_fields = ["titolo", "autore_discussione"]
    #list_filter = ["sezione_appartenenza", "data_creazione"]



class ValoriTmaAdmin(admin.ModelAdmin):
    model = ValoriTma
    list_display = ["productNumber", "layer", "dlAttenuation", "dlTrafficDelay", "ulTrafficDelay",  "tma_type", "subunit"] 
    #list_display = ["titolo", "sezione_appartenenza", "autore_discussione"]
    #search_fields = ["titolo", "autore_discussione"]
    #list_filter = ["sezione_appartenenza", "data_creazione"]


admin.site.register(Adpr, AdprModelAdmin)
admin.site.register(Scan, ScanModelAdmin)
admin.site.register(ValoriTma, ValoriTmaAdmin)