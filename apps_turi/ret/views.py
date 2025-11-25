import os
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from .models import RET, CellRet, SwapMatrix, FindBanda, TmplRet, ScriptRet, ScriptRetLog
from .forms import MyModelFormSet, ScriptRetModelForm, ScriptRetModelForm1, SwapMatrixForm, CellRetFormSet
from django.forms import modelformset_factory
from importa.models import Adpr, Scan
from django.forms.widgets import TextInput
from django import forms

def delete_allret(request):
    objs = RET.objects.filter(utente=request.user.id)
    objs.delete()

    return redirect('view_ret')

def edit_ret(request):
    adpr = Adpr.objects.filter(utente=request.user.id).order_by('pk')
    scan = Scan.objects.filter(type='RET', utente=request.user.id)
    objs = RET.objects.filter(utente=request.user.id)
    objs.delete()
    objcell = CellRet.objects.filter(utente=request.user.id)
    objcell.delete()

    cell=""
    bb_acq = False
    mimo = False
    lte700 = False

    for item in adpr:

        if item.mimo == "MIMO2x4":
            lte700 = True

        if item.mimo == "MIMO4x4":
            mimo = True

        if item.layer!="primo":

            if bb_acq:
                bb_insert = bb
                bb_acq = False
            else:
                bb_insert = item.bb    

            cell=cell+item.cella[4:6]


            if mimo or lte700:

                if mimo:
                    cella = cell + "_1"
                else:
                    
                    cella = "G" + cell[1:2]   


                value = CellRet(
                    item.pk,
                    False,
                    bb_insert,
                    #cell + "_1",
                    cella,
                    item.seq,
                    item.rusref,
                    item.mimo,
                    item.tilt,
                    request.user.id,
                    item.sistema
                    )
                value.save()

                #if item.mimo != "MIMO4x4":
                if item.mimo != "MIMO4x4" and item.mimo != "MIMO2x4":    
                    if not lte700:
                        cell=cell[0:2]
                    

                if mimo:
                    cella = cell + "_2"
                else:
                    cella = cell                


                value = CellRet(
                    item.pk + 1,
                    False,
                    bb_insert,
                    #cell + "_2",
                    cella,
                    item.seq,
                    item.rusref,
                    item.mimo,
                    item.tilt,
                    request.user.id,
                    item.sistema
                    )
                value.save()
            else:
                value = CellRet(
                    item.pk,
                    False,
                    bb_insert,
                    cell,
                    item.seq,
                    item.rusref,
                    item.mimo,
                    item.tilt,
                    request.user.id,
                    item.sistema
                    )
                value.save()
            
            
            lte700 = False
            mimo = False
            cell=""
            
        else:

            bb = item.bb
            bb_acq = True
            cell=item.cella[4:6] + "-"   


    for elem in scan:
        value = RET(
            elem.pk,
            elem.bb,
            elem.radio,
            elem.port,
            elem.unique_id,
            "",
            "",
            "",
            adpr[0].sistema,
            request.user.id
        )       
        value.save()


    #eliminazione duplicati serial number
    retA = RET.objects.filter(port="A")
    retB = RET.objects.filter(port="B")
    retR = RET.objects.filter(port="R")
    for elretR in retR:
        for elretA in retA:
            if elretA.serial == elretR.serial:
                elretA.serial="delete"
                elretA.save()
        for elretB in retB:
            if elretB.serial == elretR.serial:
                elretB.serial="delete"
                elretB.save()        
    RET.objects.filter(serial="delete").delete()



    if scan.exists():
        #return redirect('view_ret')
        return redirect('edit_cell')
    else:
        #return redirect('view_ret')
        return redirect('edit_cell2') 
        #return redirect('edit_cell3')     

def view_ret(request):
    objcell = CellRet.objects.filter(utente=request.user.id)
    CHOICES = [('', '')] + [(obj.cell, obj.cell) for obj in objcell]

    RecordFormSet = modelformset_factory(RET, formset=MyModelFormSet,                                                                                                                                                      
                                         fields=('id', 'bb', 'radio', 'port', 'serial', 'cell', 'seq', 'tilt', 'utente'), 
                                         labels={'id':'', 'bb':'', 'radio':'', 'port':'', 'serial':'', 'cell':'', 'seq':'', 'tilt':'', 'utente':''},                                                                                   
                                         can_delete=True, 
                                         extra=1, 
                                         widgets={'bb': TextInput(attrs={'size': '6'}),
                                                  'radio': TextInput(attrs={'size': '5'}),
                                                  'port': TextInput(attrs={'size': '4'}),
                                                  'serial': TextInput(attrs={'size': '25'}),
                                                  'cell': forms.Select(choices=CHOICES),      
                                                  'seq': TextInput(attrs={'size': '5'}),
                                                  'tilt': TextInput(attrs={'size': '5'}),
                                                  'utente': TextInput(attrs={'size': '5'}),
                                               
                                                },)
                                                           
    if request.method == 'POST':
        formset = RecordFormSet(request.POST, queryset=RET.objects.filter(utente=request.user.id))

        if formset.is_valid():
            formset.save()

            rets=RET.objects.filter(utente=request.user.id)

            for item in rets:
                if item.cell!="":
                    item.seq = objcell.filter(cell=item.cell)[0].seq
                    item.tilt = objcell.filter(cell=item.cell)[0].tilt
                    item.ordine = objcell.filter(cell=item.cell)[0].ordine

                else:
                    item.seq =""
                    item.tilt =""    
                item.save()

            return redirect('view_ret')

    else:
        formset = RecordFormSet(queryset=RET.objects.filter(utente=request.user.id))
      
    return render(request, 'ret/view_ret.html', {'formset': formset})

def view_ret2(request):
    objcell = CellRet.objects.filter(utente=request.user.id)
    CHOICES = [('', '')] + [(obj.cell, obj.cell) for obj in objcell]

    RecordFormSet = modelformset_factory(RET, formset=MyModelFormSet, 
                                         fields=('bb', 'radio', 'port', 'serial', 'cell', 'seq', 'tilt', 'utente'), 
                                         labels={'bb':'', 'radio':'', 'port':'', 'serial':'', 'cell':'', 'seq':'', 'tilt':'', 'utente':''},                                                                                 
                                         can_delete=True, 
                                         extra=1, 
                                         widgets={'bb': TextInput(attrs={'size': '5'}),
                                                  'radio': TextInput(attrs={'size': '5'}),
                                                  'port': TextInput(attrs={'size': '4'}),
                                                  'serial': TextInput(attrs={'size': '25'}),
                                                  'cell': forms.Select(choices=CHOICES),      
                                                  'seq': TextInput(attrs={'size': '5'}),
                                                  'tilt': TextInput(attrs={'size': '5'}),
                                                  'utente': TextInput(attrs={'size': '5'}),                                               
                                                },)
                                                           
    if request.method == 'POST':
        formset = RecordFormSet(request.POST, queryset=RET.objects.filter(utente=request.user.id))

        if formset.is_valid():
            formset.save()

            rets=RET.objects.filter(utente=request.user.id)

            for item in rets:
                if item.cell!="":
                    item.seq = objcell.filter(cell=item.cell)[0].seq
                else:
                    item.seq =""    
                item.save()

            return redirect('view_ret')
    else:
        formset = RecordFormSet(queryset=RET.objects.filter(utente=request.user.id))
      
    return render(request, 'ret/view_ret2.html', {'formset': formset})    

def edit_cell(request):
    RecordFormSet = modelformset_factory(CellRet, formset=MyModelFormSet, 
                                         fields=('master', 'bb', 'cell', 'seq', "radio", 'utente'), 
                                         labels={'master':'','bb':'','cell':'', 'seq':'', 'radio':'', 'utente':''},                                                                                 
                                         can_delete=True, 
                                         extra=1, 
                                         widgets={'bb': TextInput(attrs={'size': '7'}),
                                                  'cell': TextInput(attrs={'size': '10'}),
                                                  'seq': TextInput(attrs={'size': '5'}),
                                                  'radio': TextInput(attrs={'size': '5'}),
                                                  'utente': TextInput(attrs={'size': '5'}),                                               
                                                },)
                                                           
    if request.method == 'POST':
        formset = RecordFormSet(request.POST, queryset=CellRet.objects.filter(utente=request.user.id))

        if formset.is_valid():
            formset.save()

            cellret = CellRet.objects.filter(utente=request.user.id)


            for elem in cellret:
                
                if elem.master:
                    
                    if elem.cell[len(elem.cell)-1:len(elem.cell)]=="1":
                        #numero= int(elem.cell[1:2])*10000+1
                        numero= int(elem.cell[1:2])*1000000+1
                    elif elem.cell[len(elem.cell)-1:len(elem.cell)]=="2":
                        #numero= int(elem.cell[1:2])*10000+2
                        numero= int(elem.cell[1:2])*1000000+2
                    else:
                        #numero= int(elem.cell[1:2])*10000
                        numero= int(elem.cell[1:2])*1000000          
                    
                else:
                    #numero= int(elem.cell[1:2])*10000+elem.pk
                    numero= int(elem.cell[1:2])*1000000+elem.pk     
                elem.ordine=numero
                elem.save()


            master = cellret.filter(master=True)

            for elma in master:
                elma.cell = elma.cell[1:2]
                for cell in cellret:
                    if cell.cell[1:2]==elma.cell:
                        cell.seq = elma.seq
                        cell.radio = elma.radio
                        cell.bb = elma.bb                        
                        cell.save()

                
            return redirect('view_ret')
    else:
        formset = RecordFormSet(queryset=CellRet.objects.filter(utente=request.user.id))
      
    return render(request, 'ret/edit_cell.html', {'formset': formset})    

def insert_serialtilt(request):
    #SerialTiltFormSet = modelformset_factory(SwapMatrix, formset=MyModelFormSet,
    SerialTiltFormSet = modelformset_factory(SwapMatrix,                                          
                                         fields=('id', 'sito', 'sttr', 'banda', 'eltlt', 'serial', "porta"), 
                                         labels={'id':'', 'sito':'','sttr':'','banda':'', 'eltlt':'',  'serial':'', 'porta':''},                                                
                                         extra=0, 
                                         widgets={'sito': TextInput(attrs={'size': '5'}),
                                                  'sttr': TextInput(attrs={'size': '1'}),
                                                  'banda': TextInput(attrs={'size': '15'}),
                                                  'eltlt': TextInput(attrs={'size': '2'}),
                                                  'serial': TextInput(attrs={'size': '20'}),
                                                  'porta': TextInput(attrs={'size': '1'}),
                                                                                                  
                                                },)
                                                           
    if request.method == 'POST':
        formset = SerialTiltFormSet(request.POST, queryset=SwapMatrix.objects.filter(utente=request.user.id))

        if formset.is_valid():
            formset.save()
        
            return redirect('view_swapmatrix')
    else:
        formset = SerialTiltFormSet(queryset=SwapMatrix.objects.filter(utente=request.user.id))
      
    return render(request, 'ret/insert_serialtilt.html', {'formset': formset}) 

def load_swapmatrix(request):
    ret = RET.objects.filter(utente=request.user.id).order_by('ordine')
    swapmatrix = SwapMatrix.objects.filter(utente=request.user.id)
    swapmatrix.delete()
    findbanda = FindBanda.objects.all()

    prima="0"
    seqp="0"
    for elem in ret:
        #trova banda e label
        cell=elem.cell.replace("_1", "_a")
        cell=cell.replace("_2", "_b")
        cell=cell.replace("1", "")
        cell=cell.replace("2", "")
        cell=cell.replace("3", "")
        cell=cell.replace("4", "")
        cell=cell.replace("5", "")
        cell=cell.replace("6", "")
        cell=cell.replace("7", "")
        cell=cell.replace("8", "")
        cell=cell.replace("9", "")
        cell=cell.replace("-", "")


        banda = findbanda.filter(cell=cell)[0].banda
        label = findbanda.filter(cell=cell)[0].label

        #trova settore e prog
        numero=str(elem.ordine)[0:1]
        if numero!=prima:
            prima=numero
            settore=numero
            #i=1
            #prog=str(i)
            if seqp!=elem.radio:
                template="@1@"
                i=1
            else:
                template="@2@"
                #banda=banda+"_S"+settore  
                i=i+1
            prog=str(i)         
        else:
            i=i+1
            prog=str(i)
            template="@2@"

        seqp=elem.radio
        
        if elem.seq!=elem.radio:
            banda=banda+"_S"+settore 

        value = SwapMatrix(
            elem.ordine,
            elem.bb,
            settore,
            elem.seq,
            #elem.radio,
            banda,
            elem.serial,
            elem.radio,
            elem.port,            
            prog,
            elem.tilt,
            label,
            template,
            elem.sistema,
            
            request.user.id
        )       
        value.save()

    #sistema template impostato prima
    dataset = SwapMatrix.objects.filter(utente=request.user.id)
    i=1
    for elm in dataset:
        end=dataset.count()-1
        if i<=end:
            if elm.tmplt=="@2@" and dataset[i].tmplt=="@1@":
                elm.tmplt="@3@"            
                elm.save()
            if elm.tmplt=="@1@" and dataset[i].tmplt=="@1@":
                elm.tmplt="@4@"
                elm.save()            
        i=i+1
        if i==dataset.count()+1:
            if elm.tmplt=="@2@":
                elm.tmplt="@3@"
                elm.save()
            if elm.tmplt=="@1@":
                elm.tmplt="@4@"
                elm.save()

    dataset = SwapMatrix.objects.filter(utente=request.user.id)        
    #return render(request, 'ret/view_swapmatrix.html', {'dataset': dataset})   
     
    return redirect('view_swapmatrix2')

def edit_cell3(request):
    RecordFormSet = modelformset_factory(CellRet, formset=MyModelFormSet, 
                                         fields=('master', 'bb', 'cell', 'seq', "radio", 'utente'), 
                                         labels={'master':'','bb':'','cell':'', 'seq':'', 'radio':'', 'utente':''},                                                                                 
                                         can_delete=True, 
                                         extra=1, 
                                         widgets={'bb': TextInput(attrs={'size': '7'}),
                                                  'cell': TextInput(attrs={'size': '10'}),
                                                  'seq': TextInput(attrs={'size': '5'}),
                                                  'radio': TextInput(attrs={'size': '5'}),
                                                  'utente': TextInput(attrs={'size': '5'}),                                               
                                                },)
                                                           
    if request.method == 'POST':
        formset = RecordFormSet(request.POST, queryset=CellRet.objects.filter(utente=request.user.id))

        if formset.is_valid():
            formset.save()

            cellret = CellRet.objects.filter(utente=request.user.id)


            for elem in cellret:
                
                if elem.master:
                    
                    if elem.cell[len(elem.cell)-1:len(elem.cell)]=="1":
                        numero= int(elem.cell[1:2])*10000+1
                    elif elem.cell[len(elem.cell)-1:len(elem.cell)]=="2":
                        numero= int(elem.cell[1:2])*10000+2
                    else:
                        numero= int(elem.cell[1:2])*10000         
                    
                else:
                    numero= int(elem.cell[1:2])*10000+elem.pk     
                elem.ordine=numero
                elem.save()

            master = cellret.filter(master=True)

            for elma in master:
                elma.cell = elma.cell[1:2]
                for cell in cellret:
                    if cell.cell[1:2]==elma.cell:
                        cell.seq = elma.seq
                        cell.radio = elma.radio
                        cell.bb = elma.bb
                        cell.save()
        
            return redirect('edit_cell3')
    else:
        queryset=CellRet.objects.filter(utente=request.user.id)
        visualizza=False
        for obj in queryset:
            if obj.master:
                visualizza=True
        
        
        formset = RecordFormSet(queryset=queryset)

        return render(request, 'ret/edit_cell_old.html', {'formset': formset, 'visualizza': visualizza})
  
def edit_cell2(request):
    RecordFormSet = modelformset_factory(CellRet, formset=MyModelFormSet, 
                                         fields=('id', 'master', 'bb', 'cell', 'seq', "radio", 'utente'), 
                                         labels={'id':'', 'master':'','bb':'','cell':'', 'seq':'', 'radio':'', 'utente':''},                                                                                 
                                         can_delete=True, 
                                         extra=1, 
                                         widgets={'bb': TextInput(attrs={'size': '7'}),
                                                  'cell': TextInput(attrs={'size': '10'}),
                                                  'seq': TextInput(attrs={'size': '5'}),
                                                  'radio': TextInput(attrs={'size': '5'}),
                                                  'utente': TextInput(attrs={'size': '5'}),                                               
                                                },)
                                                           
    if request.method == 'POST':
        formset = RecordFormSet(request.POST, queryset=CellRet.objects.filter(utente=request.user.id))

        if formset.is_valid():
            formset.save()

            cellret = CellRet.objects.filter(utente=request.user.id)


            for elem in cellret:
                
                if elem.master:
                    
                    if elem.cell[len(elem.cell)-1:len(elem.cell)]=="1":
                        #numero= int(elem.cell[1:2])*10000+1
                        numero= int(elem.cell[1:2])*1000000+1
                    elif elem.cell[len(elem.cell)-1:len(elem.cell)]=="2":
                        #numero= int(elem.cell[1:2])*10000+2
                        numero= int(elem.cell[1:2])*1000000+2
                    else:
                        #numero= int(elem.cell[1:2])*10000
                        numero= int(elem.cell[1:2])*1000000 

                    if elem.cell[0:1]=="G":
                        numero = numero - 1            
                    
                else:
                    #numero= int(elem.cell[1:2])*10000+elem.pk
                    numero= int(elem.cell[1:2])*1000000+elem.pk     
                elem.ordine=numero
                elem.save()

            master = cellret.filter(master=True)

            for elma in master:
                elma.cell = elma.cell[1:2]
                for cell in cellret:
                    if cell.cell[1:2]==elma.cell:
                        cell.seq = elma.seq
                        cell.radio = elma.radio
                        cell.bb = elma.bb
                        cell.save()
        
            return redirect('edit_cell2')
    else:
        queryset=CellRet.objects.filter(utente=request.user.id)
        visualizza=False
        for obj in queryset:
            if obj.master:
                visualizza=True
        
        
        formset = RecordFormSet(queryset=queryset)

        return render(request, 'ret/edit_cell.html', {'formset': formset, 'visualizza': visualizza})
  
def load_swapmatrix2(request):
    cellret = CellRet.objects.filter(utente=request.user.id).order_by('ordine')
    swapmatrix = SwapMatrix.objects.filter(utente=request.user.id)
    swapmatrix.delete()
    findbanda = FindBanda.objects.all()

    prima="0"
    for elem in cellret:
        #trova banda e label
        cell=elem.cell.replace("_1", "_a")
        cell=cell.replace("_2", "_b")
        cell=cell.replace("1", "")
        cell=cell.replace("2", "")
        cell=cell.replace("3", "")
        cell=cell.replace("4", "")
        cell=cell.replace("5", "")
        cell=cell.replace("6", "")
        cell=cell.replace("7", "")
        cell=cell.replace("8", "")
        cell=cell.replace("9", "")
        cell=cell.replace("-", "")

        #print(cell)

        banda = findbanda.filter(cell=cell)[0].banda
        label = findbanda.filter(cell=cell)[0].label

        #trova settore e prog

        if (str(elem.ordine)[1])=="9":
            numero=str(elem.ordine + 1000000 )[0:1]
        else:
            numero=str(elem.ordine)[0:1]
        
        if numero!=prima:
            prima=numero
            settore=numero
            i=1
            prog=str(i)
            template="@1@"
        else:
            i=i+1
            prog=str(i)
            template="@2@"

        print(prog + " - " + str(elem.ordine))

        value = SwapMatrix(
            elem.ordine,
            elem.bb,
            settore,
            elem.seq,
            banda,
            "",
            elem.radio,
            "R",         
            prog,
            elem.tilt,
            label,
            template,
            elem.sistema,
            request.user.id
        )       
        value.save()

    #sistema template impostato prima
    dataset = SwapMatrix.objects.filter(utente=request.user.id)
    i=1
    for elm in dataset:
        end=dataset.count()-1
        if i<=end:
            if elm.tmplt=="@2@" and dataset[i].tmplt=="@1@":
                elm.tmplt="@3@"            
                elm.save()
            if elm.tmplt=="@1@" and dataset[i].tmplt=="@1@":
                elm.tmplt="@4@"
                elm.save()            
        i=i+1
        if i==dataset.count()+1:
            if elm.tmplt=="@2@":
                elm.tmplt="@3@"
                elm.save()
            if elm.tmplt=="@1@":
                elm.tmplt="@4@"
                elm.save()

    dataset = SwapMatrix.objects.filter(utente=request.user.id)
      
    #return render(request, 'ret/view_swapmatrix.html', {'dataset': dataset})  
    return redirect('view_swapmatrix2')

def crea_scrpit_ret(request):

    swapmatrix = SwapMatrix.objects.filter(utente=request.user.id)
    tmplret = TmplRet.objects.all()

    bb1 = swapmatrix[0].sito
    for obj in swapmatrix:
        if bb1 != obj.sito:
            bb2 = obj.sito

    retbb1 = SwapMatrix.objects.filter(sito=bb1, utente=request.user.id)
    try:        
        retbb2 = SwapMatrix.objects.filter(sito=bb2, utente=request.user.id)
    except:
        bb2 = ""    

    script1 = ""
    script2 = ""

    sito = bb1

    #script1 = "### script da caricare nella BB " + bb1 + " ###" + "\n"
    for elem in retbb1:
        elem.tmplt
        elaborato = tmplret.filter(cod=elem.tmplt)[0].tmpl
        elaborato = elaborato.replace('SITO', elem.sito)
        elaborato = elaborato.replace('STTR', elem.sttr)
        elaborato = elaborato.replace('SECEQ', elem.seceq)
        elaborato = elaborato.replace('BANDA', elem.banda)
        elaborato = elaborato.replace('SERIAL', elem.serial)
        elaborato = elaborato.replace('RADCTRL', elem.radctrl)
        elaborato = elaborato.replace('PORTA', elem.porta)
        elaborato = elaborato.replace('PROG', elem.prog)
        elaborato = elaborato.replace('ELTLT', elem.eltlt)
        elaborato = elaborato.replace('USRLBL', elem.usrlbl)
        elaborato = elaborato.replace('SISTEMA', elem.sistema)
        script1 = script1 + elaborato + "\n" + "\n" 


    if bb2 != "":
        #script2 = "### script da caricare nella BB " + bb2 + " ###" + "\n"
        for elem in retbb2:
            elem.tmplt
            elaborato = tmplret.filter(cod=elem.tmplt)[0].tmpl
            elaborato = elaborato.replace('SITO', elem.sito)
            elaborato = elaborato.replace('STTR', elem.sttr)
            elaborato = elaborato.replace('SECEQ', elem.seceq)
            elaborato = elaborato.replace('BANDA', elem.banda)
            elaborato = elaborato.replace('SERIAL', elem.serial)
            elaborato = elaborato.replace('RADCTRL', elem.radctrl)
            elaborato = elaborato.replace('PORTA', elem.porta)
            elaborato = elaborato.replace('PROG', elem.prog)
            elaborato = elaborato.replace('ELTLT', elem.eltlt)
            elaborato = elaborato.replace('USRLBL', elem.usrlbl)
            elaborato = elaborato.replace('SISTEMA', elem.sistema)
            script2 = script2 + elaborato + "\n" + "\n"

    #print(script1)
    #scrive gli sripts nel data base
    tutto = ScriptRet.objects.filter(utente=request.user.id)
    tutto.delete()
    idx=request.user.id
    elemento = ScriptRet(
        idx,
        sito,
        script1,
        script2,
        bb1,
        bb2,
        request.user.id
    )       
    elemento.save()


    return HttpResponseRedirect("/ret/view-script-ret/")      

def view_script_ret(request):

    script = ScriptRet.objects.filter(utente=request.user.id)
        
    sito=script[0].sito
    script1=script[0].script1
    script2=script[0].script2
    bb1=script[0].bb1
    bb2=script[0].bb2
  
    form_risposta = ScriptRetModelForm()
    context = {
        "sito": sito,
        "script1": script1,
        "script2": script2,
        "bb1": bb1,
        "bb2": bb2,
        "form_risposta": form_risposta,
    }

    return render(request, 'ret/view_script_ret.html', context)          

def modifica_script_ret(request):
        # dictionary for initial data with
    # field names as keys
    context ={}
 
    # fetch the object related to passed id
    obj = get_object_or_404(ScriptRet, id=request.user.id)
    
    # pass the object as instance in form
    if obj.bb2 == "":
        form = ScriptRetModelForm1(request.POST or None, instance = obj)
    else:
        form = ScriptRetModelForm(request.POST or None, instance = obj)          
 
    # save the data from the form and
    # redirect to detail_view
    if form.is_valid():
        form.save()
        #return HttpResponseRedirect("/import/"+id)
        return HttpResponseRedirect("/ret/view-script-ret/")
 
    # add form dictionary to context
    context["form"] = form
 
    return render(request, "ret/modifica_script_ret.html", context)  

def export_script1_ret(request):

    script = ScriptRet.objects.filter(utente=request.user.id)

    sito=script[0].sito
    bb1=script[0].bb1
    script=script[0].script1
    
    nomefile = bb1 + "_ret.txt"
    #nomefile = bb1 + "_ret.mos"
    #nomefile = bb1 + ".txt"
    
    response = HttpResponse(content_type='text/plain')
    response['Content-Disposition'] = f'attachment; filename="{nomefile}"'

    with open(nomefile, 'w') as f:
        f.write(script)

    with open(nomefile, 'r') as f:
        file_data = f.read()
        response.write(file_data)

    os.remove(nomefile)



    tabella = ScriptRetLog.objects.exists()

    if tabella:
        ultimo = ScriptRetLog.objects.last()
        idx = ultimo.pk + 1
    else:
        idx = 1
   
    elemento = ScriptRetLog(
        idx,
        sito[0:4],
        bb1,
        script,
        request.user.id
    )       
    elemento.save()    

    return response

def export_script2_ret(request):

    script = ScriptRet.objects.filter(utente=request.user.id)

    sito=script[0].sito
    bb2=script[0].bb2
    script=script[0].script2
    
    nomefile = bb2 + "_ret.txt"
    #nomefile = bb2 + "_ret.mos"
    #nomefile = bb2 + ".txt"
    
    response = HttpResponse(content_type='text/plain')
    response['Content-Disposition'] = f'attachment; filename="{nomefile}"'

    with open(nomefile, 'w') as f:
        f.write(script)

    with open(nomefile, 'r') as f:
        file_data = f.read()
        response.write(file_data)

    os.remove(nomefile)

    tabella = ScriptRetLog.objects.exists()

    if tabella:
        ultimo = ScriptRetLog.objects.last()
        idx = ultimo.pk + 1
    else:
        idx = 1
   
    elemento = ScriptRetLog(
        idx,
        sito[0:4],
        bb2,
        script,
        request.user.id
    )       
    elemento.save() 

    return response

def view_swapmatrix(request):
    
    dataset = SwapMatrix.objects.filter(utente=request.user.id)  
    return render(request, 'ret/view_swapmatrix.html', {'dataset': dataset})  

def view_swapmatrix2(request):
    SwapMatrixFormSet = modelformset_factory(SwapMatrix,                                          
                                         fields=('id', 'sito', 'sttr', 'seceq', 'banda', 'serial', 'radctrl', "porta", 'prog', 'eltlt', 'usrlbl', "tmplt"), 
                                         labels={'id':'', 'sito':'','sttr':'','seceq':'', 'banda':'',  'serial':'',  'radctrl':'', 'porta':'','prog':'', 'eltlt':'', 'usrlbl':'', 'tmplt':''},                                                
                                         extra=0, 
                                         widgets={'sito': TextInput(attrs={'size': '10'}),
                                                  'sttr': TextInput(attrs={'size': '1'}),
                                                  'seceq': TextInput(attrs={'size': '5'}),
                                                  'banda': TextInput(attrs={'size': '17'}),
                                                  'serial': TextInput(attrs={'size': '22'}),
                                                  'radctrl': TextInput(attrs={'size': '5'}),
                                                  'porta': TextInput(attrs={'size': '1'}),  
                                                  'prog': TextInput(attrs={'size': '1'}),
                                                  'eltlt': TextInput(attrs={'size': '2'}),
                                                  'usrlbl': TextInput(attrs={'size': '8'}),
                                                  'tmplt': TextInput(attrs={'size': '5'}),
                                                                                                  
                                                },)
                                                           
    if request.method == 'POST':
        formset = SwapMatrixFormSet(request.POST, queryset=SwapMatrix.objects.filter(utente=request.user.id))

        if formset.is_valid():
            formset.save()
        

            return redirect('view_swapmatrix2')
    else:
        formset = SwapMatrixFormSet(queryset=SwapMatrix.objects.filter(utente=request.user.id))
      
    return render(request, 'ret/view_swapmatrix2.html', {'formset': formset}) 

def update_swapmatrix(request, id):

    context ={}

    obj = get_object_or_404(SwapMatrix, id = id)

    form = SwapMatrixForm(request.POST or None, instance = obj)

    if form.is_valid():
        form.save()
        return HttpResponseRedirect("/ret/view-swapmatrix/")

    context["form"] = form
 
    return render(request, "ret/update_swapmatrix.html", context)    