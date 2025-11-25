from django.contrib import admin
from .models import  RET, CellRet, SwapMatrix, FindBanda, TmplRet, ScriptRet, ScriptRetLog

# Register your models here.


class RETModelAdmin(admin.ModelAdmin):
    model = RET
    list_display = ["bb", "radio", "port", "serial", "cell", "seq", "tilt", "sistema","utente", "ordine"]
    #list_display = ["bb", "radio", "port", "serial"]

class CellRetModelAdmin(admin.ModelAdmin):
    model = CellRet
    list_display = ["id", "master", "bb", "cell", "seq", "radio", "mimo", "tilt", "utente", "sistema", "ordine"]
    #list_display = ["bb", "radio", "port", "serial"]    

class SwapMatrixModelAdmin(admin.ModelAdmin):
    model = SwapMatrix
    list_display = ["sito", "sttr", "seceq", "banda", "serial", "radctrl", "porta", "prog", "eltlt", "usrlbl", "tmplt", "sistema", "utente"]
    #list_display = ["bb", "radio", "port", "serial"] 

class FindBandaModelAdmin(admin.ModelAdmin):
    model = FindBanda
    list_display = ["cell", "banda", "label"]
    #list_display = ["bb", "radio", "port", "serial"]    

class TmplRetAdmin(admin.ModelAdmin):
    model = TmplRet
    list_display = ["cod", "tmpl"] 
    #list_display = ["titolo", "sezione_appartenenza", "autore_discussione"]
    #search_fields = ["titolo", "autore_discussione"]
    #list_filter = ["sezione_appartenenza", "data_creazione"]

class ScriptRetModelAdmin(admin.ModelAdmin):
    model = ScriptRet
    list_display = ["sito", "script1", "script2", "bb1", "bb2", "utente"]

class ScriptRetLogModelAdmin(admin.ModelAdmin):
    model = ScriptRetLog
    list_display = ["id", "sito", "bb", "script", "time", "utente"]    


admin.site.register(TmplRet, TmplRetAdmin)  
admin.site.register(RET, RETModelAdmin)
admin.site.register(CellRet, CellRetModelAdmin)
admin.site.register(SwapMatrix, SwapMatrixModelAdmin)
admin.site.register(FindBanda, FindBandaModelAdmin)
admin.site.register(ScriptRet, ScriptRetModelAdmin)
admin.site.register(ScriptRetLog, ScriptRetLogModelAdmin)