import os
from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView
from django.http import HttpResponseBadRequest, HttpResponseRedirect, HttpResponse
from importa.models import Adpr, Scan, ValoriTma
from .models import ScriptTma, ScriptTmaLog
from .models import Tma, DeMatrix
from .forms import ScriptTmaModelForm, TmaForm, ScriptTmaModelForm, ScriptTmaModelForm1
from manutenzione.models import TmplTma
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.models import User
from django.db.models.functions import Cast
from django.db.models import IntegerField
from .forms import MyModelFormSet
from django.forms import modelformset_factory
from django.shortcuts import render, redirect  # Importa render e redirect
from django.contrib.auth.decorators import login_required  # Importa login_required
from django.forms.widgets import TextInput


def primaassocia_tma(request):

    tutto = Tma.objects.filter(utente=request.user.id)
    tutto.delete()

    return HttpResponseRedirect("/elabora/tma-view/") 

def associaTma(request):

    tutto = Tma.objects.filter(utente=request.user.id)
    tutto.delete() 
    adpr = Adpr.objects.filter(tma="SI", utente=request.user.id).order_by('pk')
    scan = Scan.objects.filter(type='TMA', utente=request.user.id)

    valoritma = ValoriTma.objects.all()

    i = 0
    mimoprec=""    
    for elem in adpr:
        i = i + 1

        dlatt = "--"
        dltrdl = "--"
        ultrdl = "--"
        tmatype = "--"
        subunit = "--" 
        serial2 = "--"           
        
        bb=elem.bb
        if elem.layer=="primo" and elem.mxmod=="SI":
            bbk=bb
        if elem.layer=="secondo" and elem.mxmod=="SI":
            print (bbk)
            bb=bbk

        scanner = scan.filter(bb=bb, seq=elem.seq, freq1tma=elem.cella[4:5])
        try:
            currenttma = valoritma.filter(productNumber=scanner[0].product_number, layer=scanner[0].freq1tma)
            serial1 = scanner[0].unique_id
            serial2 = "--"
            radio = scanner[0].radio
            port = scanner[0].port
            entra = True

        except: 
            try:
                scanner = scan.filter(bb=bb, seq=elem.rusref, freq1tma=elem.cella[4:5])
                currenttma = valoritma.filter(productNumber=scanner[2].product_number, layer=scanner[0].freq1tma)
                serial1 = scanner[2].unique_id
                serial2 = "--"
                radio = scanner[2].radio
                port = scanner[2].port
                entra = True
            except:

                dlatt = "--"
                dltrdl = "--"
                ultrdl = "--"
                tmatype = "--"
                subunit = "--"
                serial1 = "--" 
                serial2 = "--"
                radio = "--"
                port = "--"
                entra = False                

        cont = 0
        try:
            for sc in scanner:
                cont = cont + 1
        except:
            cont = 0


        cont1 = 0
        try:
            for ct in currenttma:
                cont1 = cont1 + 1  
        except:
            cont1 = 0


        if cont1 > 0 and entra:
            dlatt = currenttma[0].dlAttenuation
            dltrdl = currenttma[0].dlTrafficDelay
            ultrdl = currenttma[0].ulTrafficDelay
            tmatype = currenttma[0].tma_type
            subunit = currenttma[0].subunit
        else:
            dlatt = "--"


        if cont > 1:
            
            if elem.mimo != "MIMO4x4" and mimoprec == "":
                if scanner[0].unique_id!=scanner[1].unique_id:
                    scanner[1].seq = str(int(scanner[1].seq) + 1)
                    scanner[1].save()                    
                serial2 = "--"
            else:
                if elem.mimo != "MIMO4x4" and mimoprec == "MIMO4x4":
                    serial2 = "--"
                    port2 = "--"                       #
                else:    
                    serial2 = scanner[1].unique_id
                    port2 = scanner[1].port                                                                                    

        else:
            serial2 = "--"  
            port2  = "--"  

        if elem.mimo=="MIMO4x4":
            value = Tma(
                elem.pk,
                elem.cella+"_a",
                elem.bb,
                elem.seq,
                radio,
                elem.rutype,
                elem.layer,
                elem.mimo,
                mimoprec,
                port,
                serial1,
                "--",
                dlatt,
                dltrdl,
                ultrdl,
                tmatype,
                subunit,
                "",
                request.user.id
            )       
            value.save()

            value1 = Tma(
                elem.pk+1,
                elem.cella+"_b",
                elem.bb,
                elem.seq,
                radio,
                elem.rutype,
                elem.layer,
                elem.mimo,
                mimoprec,
                port2,
                serial2,
                "--",
                dlatt,
                dltrdl,
                ultrdl,
                tmatype,
                subunit,
                "",
                request.user.id
            )       
            value1.save()
        else:
            value = Tma(
                elem.pk,
                elem.cella,
                elem.bb,
                elem.seq,
                radio,
                elem.rutype,
                elem.layer,
                elem.mimo,
                mimoprec,
                port,
                serial1,
                serial2,
                dlatt,
                dltrdl,
                ultrdl,
                tmatype,
                subunit,
                "",
                request.user.id
            )       
            value.save()

        mimoprec=elem.mimo

    return HttpResponseRedirect("/elabora/tma-view/")

def tma_view(request):
    # dictionary for initial data with
    # field names as keys
    
    
    ### Cerca template giusto da associare
    dematrix = DeMatrix.objects.all()
    tmatbl = Tma.objects.filter(utente=request.user.id)        
    for eltmatbl in tmatbl:            
        if eltmatbl.seq==eltmatbl.radio:
            seqrefr="SI"
        else:
            seqrefr="NO"     
        
        try:       
            eltmatbl.codtmpl=dematrix.filter(tmatype=eltmatbl.tmatype, subunit=eltmatbl.subunit, layer=eltmatbl.layer, seqsref=seqrefr, cellafr=eltmatbl.cella[4:5], cellaly=eltmatbl.cella[7:8], mimo44=eltmatbl.mimo, mimo44p=eltmatbl.mimop)[0].cdtmpl
            eltmatbl.tsua=dematrix.filter(tmatype=eltmatbl.tmatype, subunit=eltmatbl.subunit, layer=eltmatbl.layer, seqsref=seqrefr, cellafr=eltmatbl.cella[4:5], cellaly=eltmatbl.cella[7:8], mimo44=eltmatbl.mimo, mimo44p=eltmatbl.mimop)[0].tsua
            eltmatbl.tsub=dematrix.filter(tmatype=eltmatbl.tmatype, subunit=eltmatbl.subunit, layer=eltmatbl.layer, seqsref=seqrefr, cellafr=eltmatbl.cella[4:5], cellaly=eltmatbl.cella[7:8], mimo44=eltmatbl.mimo, mimo44p=eltmatbl.mimop)[0].tsub
            eltmatbl.laye2=dematrix.filter(tmatype=eltmatbl.tmatype, subunit=eltmatbl.subunit, layer=eltmatbl.layer, seqsref=seqrefr, cellafr=eltmatbl.cella[4:5], cellaly=eltmatbl.cella[7:8], mimo44=eltmatbl.mimo, mimo44p=eltmatbl.mimop)[0].laye2
            eltmatbl.save()
        except:
            eltmatbl.codtmpl="--"
            eltmatbl.save()    
    
    
    #context ={}
 
    # add the dictionary during initialization
    #context["dataset"] = Tma.objects.filter(utente=request.user.id)

    #return render(request, "elabora/tma_view.html", context) 
    return redirect('tma_view2')

@login_required  # Requisito di accesso per visualizzare la vista
def tma_view2(request):
    # Crea un formset basato sul modello Tabella e sulla classe MyModelFormSet personalizzata
    RecordFormSet = modelformset_factory(Tma, formset=MyModelFormSet, 
                                         fields=('cella', 'bb', 'seq', 'radio', 'layer', 'mimo', 'mimop', 'port', 'serial1', 'serial2', 'dlAttenuation', 'dlTrafficDelay', 'ulTrafficDelay', 'tmatype', 'subunit', 'codtmpl', 'utente'), 
                                         labels={'cella':'','bb':'','seq':'','radio':'','layer':'', 'mimo':'','mimop':'','port':'','serial1':'','serial2':'','dlAttenuation':'','dlTrafficDelay':'','ulTrafficDelay':'', 'tmatype':'','subunit':'','codtmpl':'','utente':''},                                                                                 
                                         can_delete=True, 
                                         extra=1, 
                                         widgets={'cella': TextInput(attrs={'size': '6'}),
                                                  'bb': TextInput(attrs={'size': '5'}),
                                                  'seq': TextInput(attrs={'size': '3'}),
                                                  'radio': TextInput(attrs={'size': '3'}),
                                                  'layer': TextInput(attrs={'size': '6'}),
                                                  'mimo': TextInput(attrs={'size': '5'}),
                                                  'mimop': TextInput(attrs={'size': '5'}),
                                                  'port': TextInput(attrs={'size': '2'}),
                                                  'serial1': TextInput(attrs={'size': '18'}),
                                                  'serial2': TextInput(attrs={'size': '18'}),
                                                  'dlAttenuation': TextInput(attrs={'size': '4'}),
                                                  'dlTrafficDelay': TextInput(attrs={'size': '4'}),
                                                  'ulTrafficDelay': TextInput(attrs={'size': '4'}),
                                                  'tmatype': TextInput(attrs={'size': '5'}),
                                                  'subunit': TextInput(attrs={'size': '3'}),                                                                                                    
                                                  'codtmpl': TextInput(attrs={'size': '5'}), 
                                                  'utente': TextInput(attrs={'size': '4'}),                                                   		                                              
                                                },)
                                                           
    if request.method == 'POST':
        # Se il metodo della richiesta è POST, gestisce il formset
        formset = RecordFormSet(request.POST, queryset=Tma.objects.filter(utente=request.user))

        if formset.is_valid():
            formset.save()  # Salva il formset se è valido             
            return redirect('tma_view2')  # Reindirizza alla vista della tabella

    else:
        # Se il metodo della richiesta non è POST, visualizza il formset vuoto
        formset = RecordFormSet(queryset=Tma.objects.filter(utente=request.user))
      
    return render(request, 'elabora/tma_view2.html', {'formset': formset})  # Renderizza il template con il formset

def delete_tmas(request):
    if request.method == 'POST':
        object_ids = request.POST.getlist('object_id') # ottieni gli ID degli oggetti selezionati
        Tma.objects.filter(id__in=object_ids).delete() # cancella gli oggetti dal database
        print(object_ids)

    return redirect('tma_view') # reindirizza all'elenco degli oggetti

def crea_script(request):    
    #tma = Tma.objects.filter(utente=request.user.id)
    adpr = Adpr.objects.filter(utente=request.user.id)
    tma = Tma.objects.filter(utente=request.user.id).exclude(codtmpl='--')
    tmpl = TmplTma.objects.all()

    bb1 = tma[0].bb
    for obj in tma:
        if bb1 != obj.bb:
            bb2 = obj.bb
 
    #tmabb1 = Tma.objects.filter(bb=bb1, utente=request.user.id).order_by('pk')
    tmabb1 = Tma.objects.filter(bb=bb1, utente=request.user.id).order_by('pk').exclude(codtmpl='--')
    try:
        #tmabb2 = Tma.objects.filter(bb=bb2, utente=request.user.id).order_by('pk')
        tmabb2 = Tma.objects.filter(bb=bb2, utente=request.user.id).order_by('pk').exclude(codtmpl='--')
    except:
        bb2 = ""

    script1 = ""
    script2 = ""

    sito = tma[0].cella[:4]

    for elem in tmabb1:
        elaborato = tmpl.filter(cod=elem.codtmpl)[0].tmpl
        elaborato = elaborato.replace('CELLA', elem.cella)
        elaborato = elaborato.replace('BSBND', elem.bb)
        elaborato = elaborato.replace('SECTOR_EQUIPMENT', elem.seq)
        elaborato = elaborato.replace('RUSECTORREF', elem.radio)
        elaborato = elaborato.replace('RADIO', elem.rutype)
        elaborato = elaborato.replace('TMADLATTENUATION', elem.dlAttenuation)
        elaborato = elaborato.replace('TMADLTRAFFICDELAY', elem.dlTrafficDelay)
        elaborato = elaborato.replace('TMAULTRAFFICDELAY', elem.ulTrafficDelay)
        elaborato = elaborato.replace('SERIAL', elem.serial1)
        elaborato = elaborato.replace('RADCTRL', elem.radio)
        elaborato = elaborato.replace('RFPORT', elem.port)
        elaborato = elaborato.replace('TMATYPE', elem.tmatype)
        elaborato = elaborato.replace('TSUA', elem.tsua)
        elaborato = elaborato.replace('TSUB', elem.tsub)
        elaborato = elaborato.replace('LAYE2', elem.laye2)
        elaborato = elaborato.replace('LAYER', elem.cella[4:5].replace('T','1800').replace('M','2100').replace('D','900').replace('E','800').replace('L','2600'))       

        try:
            if adpr.filter(cella=elem.cella)[0].atdl != "":
                elaborato = elaborato.replace('ATDL', str(int(adpr.filter(cella=elem.cella)[0].atdl)-120))
                elaborato = elaborato.replace('RTEL', str(int(adpr.filter(cella=elem.cella)[0].rtel)+220))
        except:
            print("Cella scartata = ", elem.cella)

        ### Trova BANDA
        #banda="--"
        banad=""
        if elem.cella[4:5]=="E" and elem.tmatype=="TMA":
            banda="800"
        if elem.cella[4:5]=="E" and elem.layer=="--" and elem.tmatype=="DTMA":
            banda="800"            
        if elem.cella[4:5]=="E" and elem.layer!="--" and elem.tmatype=="DTMA":
            banda="800_900"
        if elem.cella[4:5]=="D" and elem.layer=="primo" and elem.tmatype=="DTMA":
            banda="800_900"
        if elem.cella[4:5]=="D" and elem.layer!="--" and elem.tmatype=="DTMA" and elem.subunit=="4":
            banda="800_900"
        if elem.cella[4:5]=="D" and elem.layer=="secondo" and elem.tmatype=="DTMA" and elem.subunit=="2":
            banda="900_800"
        if elem.cella[4:5]=="D" and elem.layer=="secondo" and elem.tmatype=="DTMA" and elem.subunit=="2":
            banad="900_800"            
        if elem.cella[4:5]=="D" and elem.tmatype=="TMA":
            banda="900"
        if elem.cella[4:5]=="D" and elem.layer=="--":
            banda="900"        
        if elem.cella[4:5]=="L" and elem.layer=="--":
            banda="2600" 
        if elem.cella[4:5]=="F" and elem.layer=="--":
            banda="1500" 
        if elem.cella[4:5]=="M" and elem.layer=="--":
            banda="2100" 
        if elem.cella[4:5]=="M" and elem.layer=="secondo" and elem.tmatype=="TMA":
            banda="2100"
        if elem.cella[4:5]=="M" and elem.layer=="secondo" and elem.tmatype=="DTMA" and elem.subunit=="2":
            banda="2100_1800"
        if elem.cella[4:5]=="M" and elem.layer=="secondo" and elem.tmatype=="DTMA" and elem.subunit=="4":
            banda="1800_2100"
        if elem.cella[4:5]=="T" and elem.layer=="--":
            banda="1800" 
        if elem.cella[4:5]=="T" and elem.layer=="primo" and elem.tmatype=="TMA":
            banda="1800"
        if elem.cella[4:5]=="T" and elem.layer=="primo" and elem.tmatype=="DTMA" and elem.mimo!="MIMO4x4":
            banda="1800_2100"
        if elem.cella[4:5]=="T" and elem.cella[7:8]=="a" and elem.layer=="primo" and elem.tmatype=="DTMA" and elem.mimo=="MIMO4x4":
            banda="1800_2100_1"
        if elem.cella[4:5]=="T" and elem.cella[7:8]=="b" and elem.layer=="primo" and elem.tmatype=="DTMA" and elem.mimo=="MIMO4x4":
            banda="1800_2100_2"
        if elem.cella[4:5]=="M" and elem.cella[7:8]=="a" and elem.layer=="secondo" and elem.tmatype=="DTMA" and elem.mimo=="MIMO4x4":
            banda="2100_1800_1"
        if elem.cella[4:5]=="M" and elem.cella[7:8]=="b" and elem.layer=="secondo" and elem.tmatype=="DTMA" and elem.mimo=="MIMO4x4":
            banda="2100_1800_2"
        if elem.cella[4:5]=="L" and elem.cella[7:8]=="a" and elem.layer=="--" and elem.tmatype=="TMA" and elem.mimo=="MIMO4x4":
            banda="2600_1"
        if elem.cella[4:5]=="L" and elem.cella[7:8]=="b" and elem.layer=="--" and elem.tmatype=="TMA" and elem.mimo=="MIMO4x4":
            banda="2600_2"
        if elem.cella[4:5]=="M" and elem.cella[7:8]=="a" and elem.layer=="secondo" and elem.tmatype=="DTMA" and elem.mimo=="MIMO4x4" and elem.subunit=="4":
            banda="1800_2100_1"
        if elem.cella[4:5]=="M" and elem.cella[7:8]=="b" and elem.layer=="secondo" and elem.tmatype=="DTMA" and elem.mimo=="MIMO4x4" and elem.subunit=="4":
            banda="1800_2100_2"            
        # fine trova BANDA
 
        elaborato = elaborato.replace('BANDA', banda)
        elaborato = elaborato.replace('BANAD', banad)


        script1 = script1 + "\n" + elaborato

    try:
        for elem in tmabb2:
            elaborato = tmpl.filter(cod=elem.codtmpl)[0].tmpl
            elaborato = elaborato.replace('CELLA', elem.cella)
            elaborato = elaborato.replace('BSBND', elem.bb)
            elaborato = elaborato.replace('SECTOR_EQUIPMENT', elem.seq)
            elaborato = elaborato.replace('RUSECTORREF', elem.radio)
            elaborato = elaborato.replace('RADIO', elem.rutype)
            elaborato = elaborato.replace('TMADLATTENUATION', elem.dlAttenuation)
            elaborato = elaborato.replace('TMADLTRAFFICDELAY', elem.dlTrafficDelay)
            elaborato = elaborato.replace('TMAULTRAFFICDELAY', elem.ulTrafficDelay)
            elaborato = elaborato.replace('SERIAL', elem.serial1)
            elaborato = elaborato.replace('RADCTRL', elem.radio)
            elaborato = elaborato.replace('RFPORT', elem.port)
            elaborato = elaborato.replace('TMATYPE', elem.tmatype)
            elaborato = elaborato.replace('TSUA', elem.tsua)
            elaborato = elaborato.replace('TSUB', elem.tsub)
            elaborato = elaborato.replace('LAYE2', elem.laye2)
            elaborato = elaborato.replace('LAYER', elem.cella[4:5].replace('T','1800').replace('M','2100').replace('D','900').replace('E','800').replace('L','2600'))

            try:
                if adpr.filter(cella=elem.cella)[0].atdl != "":
                    elaborato = elaborato.replace('ATDL', str(int(adpr.filter(cella=elem.cella)[0].atdl)-120))
                    elaborato = elaborato.replace('RTEL', str(int(adpr.filter(cella=elem.cella)[0].rtel)+220))
            except:
                print("Cella scartata = ", elem.cella)


            ### Trova BANDA
            banad=""
            if elem.cella[4:5]=="E" and elem.tmatype=="TMA":
                banda="800"
            if elem.cella[4:5]=="E" and elem.layer!="--" and elem.tmatype=="DTMA":
                banda="800_900"
            if elem.cella[4:5]=="D" and elem.layer=="primo" and elem.tmatype=="DTMA":
                banda="800_900"
            if elem.cella[4:5]=="D" and elem.layer!="--" and elem.tmatype=="DTMA" and elem.subunit=="4":
                banda="800_900"
            if elem.cella[4:5]=="D" and elem.layer=="secondo" and elem.tmatype=="DTMA" and elem.subunit=="2":
                banda="900_800"
            if elem.cella[4:5]=="D" and elem.layer=="secondo" and elem.tmatype=="DTMA" and elem.subunit=="2":
                banad="900_800" 
            if elem.cella[4:5]=="D" and elem.tmatype=="TMA":
                banda="900"
            if elem.cella[4:5]=="D" and elem.layer=="--":
                banda="900"        
            if elem.cella[4:5]=="L" and elem.layer=="--":
                banda="2600" 
            if elem.cella[4:5]=="F" and elem.layer=="--":
                banda="1500" 
            if elem.cella[4:5]=="M" and elem.layer=="--":
                banda="2100" 
            if elem.cella[4:5]=="M" and elem.layer=="secondo" and elem.tmatype=="TMA":
                banda="2100"
            if elem.cella[4:5]=="M" and elem.layer=="secondo" and elem.tmatype=="DTMA" and elem.subunit=="2":
                banda="2100_1800"
            if elem.cella[4:5]=="M" and elem.layer=="secondo" and elem.tmatype=="DTMA" and elem.subunit=="4":
                banda="1800_2100"
            if elem.cella[4:5]=="T" and elem.layer=="--":
                banda="1800" 
            if elem.cella[4:5]=="T" and elem.layer=="primo" and elem.tmatype=="TMA":
                banda="1800"
            if elem.cella[4:5]=="T" and elem.layer=="primo" and elem.tmatype=="DTMA" and elem.mimo!="MIMO4x4":
                banda="1800_2100"
            if elem.cella[4:5]=="T" and elem.cella[7:8]=="a" and elem.layer=="primo" and elem.tmatype=="DTMA" and elem.mimo=="MIMO4x4":
                banda="1800_2100_1"
            if elem.cella[4:5]=="T" and elem.cella[7:8]=="b" and elem.layer=="primo" and elem.tmatype=="DTMA" and elem.mimo=="MIMO4x4":
                banda="1800_2100_2"
            if elem.cella[4:5]=="M" and elem.cella[7:8]=="a" and elem.layer=="secondo" and elem.tmatype=="DTMA" and elem.mimo=="MIMO4x4":
                banda="2100_1800_1"
            if elem.cella[4:5]=="M" and elem.cella[7:8]=="b" and elem.layer=="secondo" and elem.tmatype=="DTMA" and elem.mimo=="MIMO4x4":
                banda="2100_1800_2"
            if elem.cella[4:5]=="L" and elem.cella[7:8]=="a" and elem.layer=="--" and elem.tmatype=="TMA" and elem.mimo=="MIMO4x4":
                banda="2600_1"
            if elem.cella[4:5]=="L" and elem.cella[7:8]=="b" and elem.layer=="--" and elem.tmatype=="TMA" and elem.mimo=="MIMO4x4":
                banda="2600_2"
            if elem.cella[4:5]=="M" and elem.cella[7:8]=="a" and elem.layer=="secondo" and elem.tmatype=="DTMA" and elem.mimo=="MIMO4x4" and elem.subunit=="4":
                banda="1800_2100_1"
            if elem.cella[4:5]=="M" and elem.cella[7:8]=="b" and elem.layer=="secondo" and elem.tmatype=="DTMA" and elem.mimo=="MIMO4x4" and elem.subunit=="4":
                banda="1800_2100_2"

            # fine trova BANDA
            elaborato = elaborato.replace('BANDA', banda)
            elaborato = elaborato.replace('BANAD', banad)

            script2 = script2 + "\n" + elaborato
    except:
            script2 = ""

    #scrive gli sripts nel data base
    tutto = ScriptTma.objects.filter(utente=request.user.id)
    tutto.delete()
    idx=request.user.id
    elemento = ScriptTma(
        idx,
        sito,
        script1,
        script2,
        bb1,
        bb2,
        request.user.id
    )       
    elemento.save()


    return HttpResponseRedirect("/elabora/view-script/")

def update_tma(request, id):
    # dictionary for initial data with
    # field names as keys
    context ={}
 
    # fetch the object related to passed id
    obj = get_object_or_404(Tma, id = id)
 
    # pass the object as instance in form
    form = TmaForm(request.POST or None, instance = obj)
 
    # save the data from the form and
    # redirect to detail_view
    if form.is_valid():
        form.save()
        #return HttpResponseRedirect("/import/"+id)
        return HttpResponseRedirect("/elabora/tma-view/")
 
    # add form dictionary to context
    context["form"] = form
 
    return render(request, "importa/update_view.html", context)    

def delete_tma(request, id):
    # dictionary for initial data with
    # field names as keys
    context ={}
 
    # fetch the object related to passed id
    obj = get_object_or_404(Tma, id = id)
 
 
    if request.method =="POST":
        # delete object
        obj.delete()
        # after deleting redirect to
        # home page
        return HttpResponseRedirect("/elabora/tma-view/")
 
    return render(request, "elabora/delete_tma.html", context)

def deleteall_tma(request):
    #tutto = Tma.objects.all()
    tutto = Tma.objects.filter(utente=request.user.id)
    tutto.delete()
    return HttpResponseRedirect("/elabora/tma-view/")

def create_tma(request):
    # dictionary for initial data with
    # field names as keys
    context ={}
 
    # add the dictionary during initialization
    form = TmaForm(request.POST or None)
    if form.is_valid():
        form.save()
        return HttpResponseRedirect("/elabora/tma-view/")
         
    context['form']= form
    return render(request, "importa/create_view.html", context)

def export_script1(request):

    script = ScriptTma.objects.filter(utente=request.user.id)

    sito=script[0].sito
    bb1=script[0].bb1
    script=script[0].script1
    
    nomefile = bb1 + "_tma.mos"
    #nomefile = bb1 + ".txt"
    
    response = HttpResponse(content_type='text/plain')
    response['Content-Disposition'] = f'attachment; filename="{nomefile}"'

    with open(nomefile, 'w') as f:
        f.write(script)

    with open(nomefile, 'r') as f:
        file_data = f.read()
        response.write(file_data)

    os.remove(nomefile)

    tabella = ScriptTmaLog.objects.exists()

    if tabella:
        ultimo = ScriptTmaLog.objects.last()
        idx = ultimo.pk + 1
    else:
        idx = 1
   
    elemento = ScriptTmaLog(
        idx,
        sito[0:4],
        bb1,
        script,
        request.user.id
    )       
    elemento.save()  



    return response

def export_script2(request):

    script = ScriptTma.objects.filter(utente=request.user.id)

    sito=script[0].sito
    bb2=script[0].bb2
    script=script[0].script2
    
    nomefile = bb2 + "_tma.mos"
    #nomefile = bb2 + ".txt"
    
    response = HttpResponse(content_type='text/plain')
    response['Content-Disposition'] = f'attachment; filename="{nomefile}"'

    with open(nomefile, 'w') as f:
        f.write(script)

    with open(nomefile, 'r') as f:
        file_data = f.read()
        response.write(file_data)

    os.remove(nomefile)

    tabella = ScriptTmaLog.objects.exists()

    if tabella:
        ultimo = ScriptTmaLog.objects.last()
        idx = ultimo.pk + 1
    else:
        idx = 1
   
    elemento = ScriptTmaLog(
        idx,
        sito[0:4],
        bb2,
        script,
        request.user.id
    )       
    elemento.save()  

    return response

def modifica_script(request):
    # dictionary for initial data with
    # field names as keys
    context ={}
 
    # fetch the object related to passed id
    obj = get_object_or_404(ScriptTma, id=request.user.id)
    
    # pass the object as instance in form
    if obj.bb2 == "":
        form = ScriptTmaModelForm1(request.POST or None, instance = obj)
    else:
        form = ScriptTmaModelForm(request.POST or None, instance = obj)          
 
    # save the data from the form and
    # redirect to detail_view
    if form.is_valid():
        form.save()
        #return HttpResponseRedirect("/import/"+id)
        return HttpResponseRedirect("/elabora/view-script/")
 
    # add form dictionary to context
    context["form"] = form
 
    return render(request, "elabora/modifica_script.html", context)  

def view_script(request):

    script = ScriptTma.objects.filter(utente=request.user.id)
        
    sito=script[0].sito
    script1=script[0].script1
    script2=script[0].script2
    bb1=script[0].bb1
    bb2=script[0].bb2
  
    form_risposta = ScriptTmaModelForm()
    context = {
        "sito": sito,
        "script1": script1,
        "script2": script2,
        "bb1": bb1,
        "bb2": bb2,
        "form_risposta": form_risposta,
    }

    return render(request, 'elabora/view_script.html', context)

def ret_view(request):
    ret = Scan.objects.filter(type='RET', utente=request.user.id).order_by(Cast('radio', IntegerField()), 'port', 'unique_id')
    context = {'ret_list': ret}

    return render(request, 'elabora/ret_view.html', context)
