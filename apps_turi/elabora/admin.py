from django.contrib import admin
from .models import Tma, DeMatrix, ScriptTma, ScriptTmaLog

# Register your models here.


class TmaModelAdmin(admin.ModelAdmin):
    model = Tma
    list_display = ["cella", "bb", "seq", "radio", "rutype", "layer", "mimo", "mimop", "port", "serial1", "serial2", "dlAttenuation", "dlTrafficDelay", "ulTrafficDelay", "tmatype", "subunit", "codtmpl", "utente", "tsua", "tsub", "laye2"] 


class DeMatrixModelAdmin(admin.ModelAdmin):
    model = DeMatrix
    list_display = ["tmatype", "subunit", "layer", "seqsref", "cellafr", "cellaly", "mimo44", "mimo44p", "tsua", "tsub", "laye2", "cdtmpl"]


class ScriptTmaModelAdmin(admin.ModelAdmin):
    model = ScriptTma
    list_display = ["sito", "script1", "script2", "bb1", "bb2", "utente"]

class ScriptTmaLogModelAdmin(admin.ModelAdmin):
    model = ScriptTmaLog
    list_display = ["id", "sito", "bb", "script", "time", "utente"]    



admin.site.register(Tma, TmaModelAdmin)
admin.site.register(DeMatrix, DeMatrixModelAdmin)
admin.site.register(ScriptTma, ScriptTmaModelAdmin)
admin.site.register(ScriptTmaLog, ScriptTmaLogModelAdmin)