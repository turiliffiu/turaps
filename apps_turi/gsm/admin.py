from django.contrib import admin
from .models import AdprGsm, TmplGsm, ScriptGsm, ScriptGsmLog
# Register your models here.

class AdprGsmModelAdmin(admin.ModelAdmin):
    model = AdprGsm
    list_display = ["cella", "bb", "bsc", "tg", "sdcch", "portanti", "utente"] 

class TmplGsmAdmin(admin.ModelAdmin):
    model = TmplGsm
    list_display = ["cod", "tmpl"] 

class ScriptGsmModelAdmin(admin.ModelAdmin):
    model = ScriptGsm
    list_display = ["sito", "script", "bb", "bsc", "utente"]

class ScriptGsmLogModelAdmin(admin.ModelAdmin):
    model = ScriptGsmLog
    list_display = ["id", "sito", "bb", "script", "time", "utente"]    





admin.site.register(AdprGsm, AdprGsmModelAdmin)
admin.site.register(TmplGsm, TmplGsmAdmin)  
admin.site.register(ScriptGsm, ScriptGsmModelAdmin)
admin.site.register(ScriptGsmLog, ScriptGsmLogModelAdmin)