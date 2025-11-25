from django.shortcuts import render


import os
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from .models import  TmplGsm, ScriptGsm, AdprGsm, ScriptGsmLog
from .forms import ScriptGsmModelForm


from django.forms import modelformset_factory
from importa.models import Adpr, Scan
from django.forms.widgets import TextInput
from django import forms
import math


# Create your views here.

def crea_script_gsm(request):

    adprgsm = AdprGsm.objects.filter(utente=request.user.id)
    tmplgsm = TmplGsm.objects.all()

    bb = adprgsm[0].bb
    bsc = adprgsm[0].bsc
    sito = bb[0:4]
    script = ""


    codtmpl = "@1@"       
    elaborato = tmplgsm.filter(cod=codtmpl)[0].tmpl
    elaborato = elaborato.replace('QQQQQ', sito)
    elaborato = elaborato.replace('JJJJJJ', bsc)
    script = script + elaborato + "\n" + "\n" 

    codtmpl = "@2@"
    for elem in adprgsm:
        elaborato = tmplgsm.filter(cod=codtmpl)[0].tmpl
        elaborato = elaborato.replace('CELLA', elem.cella)
        script = script + elaborato + "\n" + "\n" 

    codtmpl = "@3@"        
    elaborato = tmplgsm.filter(cod=codtmpl)[0].tmpl
    script = script + elaborato + "\n" + "\n" 

    codtmpl = "@4@"
    for elem in adprgsm:
        elaborato = tmplgsm.filter(cod=codtmpl)[0].tmpl
        elaborato = elaborato.replace('CELLA', elem.cella)
        elaborato = elaborato.replace('XXXX', elem.tg)
        elaborato = elaborato.replace('KKKKK', elem.cella[0:5])
        elaborato = elaborato.replace('ZZ', elem.cella[5:6])
        script = script + elaborato + "\n" + "\n" 

    codtmpl = "@5@"        
    elaborato = tmplgsm.filter(cod=codtmpl)[0].tmpl
    script = script + elaborato + "\n" + "\n" 

    codtmpl = "@6@"
    for elem in adprgsm:
        elaborato = tmplgsm.filter(cod=codtmpl)[0].tmpl
        elaborato = elaborato.replace('CELLA', elem.cella)
        script = script + elaborato + "\n" 

    script = script + "\n"

    codtmpl = "@7@"
    for elem in adprgsm:
        elaborato = tmplgsm.filter(cod=codtmpl)[0].tmpl
        elaborato = elaborato.replace('CELLA', elem.cella)
        script = script + elaborato + "\n" 

    script = script + "\n"

    codtmpl = "@8@"
    for elem in adprgsm:
        elaborato = tmplgsm.filter(cod=codtmpl)[0].tmpl
        elaborato = elaborato.replace('CELLA', elem.cella)
        script = script + elaborato + "\n" 

    script = script + "\n"

    codtmpl = "@9@"        
    elaborato = tmplgsm.filter(cod=codtmpl)[0].tmpl
    script = script + elaborato + "\n" + "\n" 

    codtmpl = "@10@"
    for elem in adprgsm:
        elaborato = tmplgsm.filter(cod=codtmpl)[0].tmpl
        elaborato = elaborato.replace('XXXX', elem.tg)
        elaborato = elaborato.replace('ZZ', elem.cella[5:6])
        script = script + elaborato + "\n" + "\n"

    codtmpl = "@11@"        
    elaborato = tmplgsm.filter(cod=codtmpl)[0].tmpl
    script = script + elaborato + "\n" + "\n" 

    codtmpl = "@12@"
    for elem in adprgsm:
        elaborato = tmplgsm.filter(cod=codtmpl)[0].tmpl
        elaborato = elaborato.replace('CELLA', elem.cella)
        script = script + elaborato + "\n" + "\n"

    codtmpl = "@13@"        
    elaborato = tmplgsm.filter(cod=codtmpl)[0].tmpl
    script = script + elaborato + "\n" + "\n" 

    codtmpl = "@14@"
    for elem in adprgsm:
        elaborato = tmplgsm.filter(cod=codtmpl)[0].tmpl
        elaborato = elaborato.replace('CELLA', elem.cella)
        script = script + elaborato + "\n" + "\n"

    codtmpl = "@15@"        
    elaborato = tmplgsm.filter(cod=codtmpl)[0].tmpl
    script = script + elaborato + "\n" + "\n" 

    codtmpl = "@16@"
    for elem in adprgsm:
        elaborato = tmplgsm.filter(cod=codtmpl)[0].tmpl
        elaborato = elaborato.replace('CELLA', elem.cella)
        script = script + elaborato + "\n" + "\n"

    codtmpl = "@17@"        
    elaborato = tmplgsm.filter(cod=codtmpl)[0].tmpl
    elaborato = elaborato.replace('QQQQQ', elem.bb)
    elaborato = elaborato.replace('JJJJJJ', elem.bsc)
    script = script + elaborato + "\n" + "\n" 

    codtmpl = "@25@"
    for elem in adprgsm:
        elaborato = tmplgsm.filter(cod=codtmpl)[0].tmpl
        elaborato = elaborato.replace('QQQQQ', elem.bb)
        elaborato = elaborato.replace('JJJJJJ', elem.bsc)
        elaborato = elaborato.replace('CELLA', elem.cella)
        elaborato = elaborato.replace('TALVA', str(int(elem.portanti)*8-int(elem.sdcch)-5))
        elaborato = elaborato.replace('TELVA', str(math.ceil(((int(elem.portanti)*8-(int(elem.portanti)*2)-1)*0.8)-1)))
        elaborato = elaborato.replace('TFLVA', str(math.ceil(((int(elem.portanti)*8-(int(elem.portanti)*2)-1)*0.3)-1)))
        script = script + elaborato + "\n"  

    codtmpl = "@26@"        
    elaborato = tmplgsm.filter(cod=codtmpl)[0].tmpl
    script = script + elaborato + "\n" + "\n" 

    codtmpl = "@18@"
    for elem in adprgsm:
        elaborato = tmplgsm.filter(cod=codtmpl)[0].tmpl
        elaborato = elaborato.replace('CELLA', elem.cella)
        script = script + elaborato + "\n"    

    codtmpl = "@19@"        
    elaborato = tmplgsm.filter(cod=codtmpl)[0].tmpl
    script = script + "\n" + elaborato + "\n" + "\n" 

    codtmpl = "@20@"
    for elem in adprgsm:
        elaborato = tmplgsm.filter(cod=codtmpl)[0].tmpl
        elaborato = elaborato.replace('CELLA', elem.cella)
        script = script + elaborato + "\n" + "\n"

    codtmpl = "@21@"
    for elem in adprgsm:
        elaborato = tmplgsm.filter(cod=codtmpl)[0].tmpl
        elaborato = elaborato.replace('CELLA', elem.cella)
        elaborato = elaborato.replace('JJJJJJ', elem.bsc)
        script = script + elaborato + "\n" 

    codtmpl = "@22@"        
    elaborato = tmplgsm.filter(cod=codtmpl)[0].tmpl
    script = script + "\n" + elaborato + "\n" + "\n"

    codtmpl = "@23@"
    for elem in adprgsm:
        elaborato = tmplgsm.filter(cod=codtmpl)[0].tmpl
        elaborato = elaborato.replace('CELLA', elem.cella)
        elaborato = elaborato.replace('XXXX', elem.tg)
        script = script + elaborato + "\n" + "\n" 

    codtmpl = "@24@"        
    elaborato = tmplgsm.filter(cod=codtmpl)[0].tmpl
    script = script + elaborato + "\n" + "\n"

    #scrive gli sripts nel data base
    tutto = ScriptGsm.objects.filter(utente=request.user.id)
    tutto.delete()
    idx=request.user.id
    elemento = ScriptGsm(
        idx,
        sito,
        script,
        bb,
        bsc,
        request.user.id
    )       
    elemento.save()


    return HttpResponseRedirect("/gsm/view-script-gsm/")    

def view_script_gsm(request):

    script = ScriptGsm.objects.filter(utente=request.user.id)
        
    sito = script[0].sito[0:4]
    bb = script[0].bb
    bsc = script[0].bsc
    scrpt = script[0].script

  
    form_risposta = ScriptGsmModelForm()
    context = {
        "sito": sito,
        "script": scrpt,
        "bb": bb,
        "bsc": bsc,
        "form_risposta": form_risposta,
    }

    return render(request, 'gsm/view_script_gsm.html', context)   

def modifica_script_gsm(request):
        # dictionary for initial data with
    # field names as keys
    context ={}
 
    # fetch the object related to passed id
    obj = get_object_or_404(ScriptGsm, id=request.user.id)
    
    # pass the object as instance in form
 
    form = ScriptGsmModelForm(request.POST or None, instance = obj)          
 
    # save the data from the form and
    # redirect to detail_view
    if form.is_valid():
        form.save()
        #return HttpResponseRedirect("/import/"+id)
        return HttpResponseRedirect("/gsm/view-script-gsm/")
 
    # add form dictionary to context
    context["form"] = form
 
    return render(request, "gsm/modifica_script_gsm.html", context)    

def export_script_gsm(request):

    script = ScriptGsm.objects.filter(utente=request.user.id)

    sito=script[0].sito
    bb=script[0].bb
    scrpt=script[0].script
    
    nomefile = sito + "_gsm.txt"
    #nomefile = bb1 + ".txt"
    
    response = HttpResponse(content_type='text/plain')
    response['Content-Disposition'] = f'attachment; filename="{nomefile}"'

    with open(nomefile, 'w') as f:
        f.write(scrpt)

    with open(nomefile, 'r') as f:
        file_data = f.read()
        response.write(file_data)

    os.remove(nomefile)

    tabella = ScriptGsmLog.objects.exists()

    if tabella:
        ultimo = ScriptGsmLog.objects.last()
        idx = ultimo.pk + 1
    else:
        idx = 1
   
    elemento = ScriptGsmLog(
        idx,
        sito[0:4],
        bb,
        scrpt,
        request.user.id
    )       
    elemento.save() 

    return response  



