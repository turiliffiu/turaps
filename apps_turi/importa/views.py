from .mixins import StaffMixing
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponseBadRequest, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views.generic.edit import CreateView, DeleteView
from django.views.generic.list import ListView
from django.shortcuts import render
from tablib import Dataset
from .models import Adpr, Scan, ValoriTma
from gsm.models import AdprGsm
from .forms import AdprForm, ScanForm
from xml.etree import ElementTree
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from .forms import MyModelFormSet
from django.forms import modelformset_factory
from django.forms.widgets import TextInput

def importAdpr(request):
    if request.method == 'POST':
        tutto = Adpr.objects.filter(utente=request.user.id)
        tutto.delete()
        tutto1 = AdprGsm.objects.filter(utente=request.user.id)
        tutto1.delete()

        lte = True
        gsm = True
        i = 0

        dataset1 = Dataset()
        try:
            adpr_lte = request.FILES['lte']
            imported_data1 = dataset1.load(adpr_lte.read(), format = "xlsx")
        except:
            lte = False    
        

        dataset2 = Dataset()
        try:
            adpr_gsm = request.FILES['gsm']
            imported_data2 = dataset2.load(adpr_gsm.read(), format = "xlsx")
        except:
            gsm = False    


        #scambia dataset in caso di caricamento al contrario
        if lte and gsm and imported_data1[0][10][4:5] == "D":
            imported_data2 = dataset1
            imported_data1 = dataset2

        if lte and gsm==False and imported_data1[0][10][4:5] == "D":
            imported_data2 = dataset1
            lte=False
            gsm=True

        if lte==False and gsm and imported_data2[0][10][4:5] != "D":
            imported_data1 = dataset2
            lte=True
            gsm=False


        if lte:
            for data1 in imported_data1:

                try:
                    dato = data1[10][4:5]
                except:
                    break    
                    
                if data1[10][4:5]=="E":
                    j=100
                elif data1[10][4:5]=="D":
                    j=102
                elif data1[10][4:5]=="T":
                    j=200
                elif data1[10][4:5]=="M":
                    j=202
                elif data1[10][4:5]=="L":
                    j=300
                elif data1[10][4:5]=="F":
                    j=400
                else:
                    j=900

                j=j+int(data1[10][5:6])*10     
                j=request.user.id*1000+j    

                i = i + 1

                indice = imported_data1.headers.index("RUSECTORREF") 
                if data1[imported_data1.headers.index("RUSECTORREF")] == "" or data1[imported_data1.headers.index("RUSECTORREF")] == None:   
                    indice = 9
                
                if data1[imported_data1.headers.index("MIMO")] == "" or data1[imported_data1.headers.index("MIMO")] == None:   
                    mimo = ""
                else:
                    mimo = data1[imported_data1.headers.index("MIMO")]                    

                try:
                    idx=imported_data1.headers.index("ELECTRICALANTENNATILT")
                except:
                    try:            
                        idx=imported_data1.headers.index("electricalAntennaTilt") # seconda scelta
                    except:
                        idx=imported_data1.headers.index("ELEcTRICALANTENNATILt") # terza scelta

                try:
                    sistema=imported_data1.headers.index("sistema")
                except:
                    try:            
                        sistema=imported_data1.headers.index("SISTEMA") # seconda scelta
                    except:
                        sistema=imported_data1.headers.index("Sistema") # terza scelta




                value1 = Adpr(
                    j,
                    data1[10],
                    data1[5],
                    data1[9],
                    data1[indice],
                    data1[imported_data1.headers.index("RU_TYPE")],
                    "--",
                    data1[13],
                    mimo,
                    data1[imported_data1.headers.index("TMA")],
                    data1[imported_data1.headers.index("RET")],
                    data1[idx],
                    "",
                    "",
                    data1[sistema][5:13],
                    request.user.id,                
                )
                value1.save()

        if gsm:
            for data2 in imported_data2:

                try:
                    dato = data2[10][4:5]
                except:
                    break                   

                if data2[10][4:5]=="E":
                    j=100
                elif data2[10][4:5]=="D":
                    j=102
                elif data2[10][4:5]=="T":
                    j=200
                elif data2[10][4:5]=="M":
                    j=202
                elif data2[10][4:5]=="L":
                    j=300
                elif data2[10][4:5]=="F":
                    j=400
                else:
                    j=900
                    
                j=j+int(data2[10][5:6])*10
                j=request.user.id*1000+j 

                i = i + 1
                indice = 194

                if data2[indice] == "" or data2[indice] == None:
                    indice = 6

                try:
                    idx=imported_data2.headers.index("ELECTRICALANTENNATILT")
                except:
                    try:            
                        idx=imported_data2.headers.index("electricalAntennaTilt") # seconda scelta
                    except:
                        idx=imported_data2.headers.index("ELEcTRICALANTENNATILt") # terza scelta

                try:
                    idx1=imported_data2.headers.index("CELLA")
                except:
                    try:            
                        idx1=imported_data2.headers.index("Cella") # seconda scelta
                    except:
                        try:
                            idx1=imported_data2.headers.index("cellA") # terza scelta
                        except:
                            idx1=imported_data2.headers.index("cella") # quarta scelta    

                try:
                    sistema=imported_data1.headers.index("sistema")
                except:
                    try:            
                        sistema=imported_data1.headers.index("SISTEMA") # seconda scelta
                    except:
                        sistema=imported_data1.headers.index("Sistema") # terza scelta



                value2 = Adpr(
                    j,
                    data2[10],
                    data2[9],
                    data2[6],
                    data2[indice],
                    data2[195],
                    "--",
                    data2[imported_data2.headers.index("MIXED_MODE")],
                    "",
                    data2[12], 
                    data2[196],                                        
                    data2[idx],
                    data2[imported_data2.headers.index("ATTENUAZIONE_CAVI_DL")],
                    data2[imported_data2.headers.index("RITARDO_ELETTRICO_BB")],
                    data2[sistema][4:12],
                    request.user.id,               
                )
                value2.save()  

                value3 = AdprGsm(
                    j,
                    data2[idx1],
                    data2[imported_data2.headers.index("RBS_NAME")],
                    data2[imported_data2.headers.index("BSC_NODE_NAME")],
                    data2[imported_data2.headers.index("BSC_TG")],
                    data2[imported_data2.headers.index("N_NUM_SDCCH")],
                    data2[imported_data2.headers.index("NUM_CHGR0_CHA")],
                    request.user.id,               
                )
                value3.save() 

        # Ricerca - primo secondo -
        if gsm or lte:
            ricerca = Adpr.objects.filter(utente=request.user.id)
            c = 0
            for rc in ricerca:
                c = c + 1            
                el = range(c, i)
                for n in el:
                    if rc.seq == ricerca[n].seq:

                        if rc.cella[4:5] == "T" or rc.cella[4:5] == "E":
                            if ricerca[n].cella[4:5] == "M" or ricerca[n].cella[4:5] == "D":                                
                                rc.layer = "primo"
                                rc.save()

                        if rc.cella[4:5] == "M" or rc.cella[4:5] == "D":
                            rc.layer = "secondo"
                            rc.save()    

                        if ricerca[n].cella[4:5] == "T" or ricerca[n].cella[4:5] == "E":
                            
                            ricerca[n].layer = "primo"
                            ricerca[n].save()

                        if ricerca[n].cella[4:5] == "M" or ricerca[n].cella[4:5] == "D":
                            ricerca[n].layer = "secondo"
                            ricerca[n].save()
                
        return HttpResponseRedirect("/importa/list-view2/")

    #return render(request, 'importa/import_adpr_modal.html')
    #return render(request, 'importa/list_view2.html')

    visualizza = True
    visualizzaelimina = False
    return render(request, 'importa/list_view2.html', {'visualizza': visualizza, 'visualizzaelimina': visualizzaelimina}) 

def importScan(request):
    if request.method == 'POST':
        tutto = Scan.objects.filter(utente=request.user.id)
        tutto.delete()
        i = 0

        # estrazione prima BB
        try:
            scan_bb1 = ElementTree.parse(request.FILES['scan1'])
            path1 = str(request.FILES['scan1'])

            ldn_bool = True
            frq1tma = "--"
            tma_bool = False
            sub2_bool = False
            sub3_bool = False
            sub5_bool = False
            salva = False
            salvaret = False
            type = None
            unique_id = None
            product_number = None
            type_p = None                       
            unique_id_p = None
            product_number_p = None

            bb1 = path1[path1.find('=')+1:path1.find(',')]            
            if len(bb1)>5:
               bb1 = bb1[:bb1.find('_')]

            for node in scan_bb1.iter():

                ldn = node.attrib.get('ldn')            
                if ldn == None:
                    ldn_bool = False
                else:
                    ldn_bool = True                
                if ldn_bool == True:
                    ldn_p = ldn
                    type_p = None
                    tma_bool = False

                port=node.attrib.get('id')
                if port == 'A' or port == 'B' or port == 'C' or port == 'D' or port == 'R':
                    port_bool = True
                else:
                    port_bool = False                
                if port_bool == True:
                    port_p = port


                type=node.attrib.get('type')
                if type != None:
                    type_p=node.attrib.get('type')[-3:]                      
                    unique_id_p=node.attrib.get('unique_id')
                    product_number_p=node.attrib.get('product_number').rstrip()

                subunit=node.attrib.get('subunit')
                FreqBand=node.attrib.get('rxFreqBand')

                if type_p == "RET":
                    salvaret = True
                    salva = True
                    frq1tma = "--" 

                if type == "TMA":
                    tma_bool = True

                if subunit == "2":
                    sub2_bool = True

                if subunit == "3":
                    sub3_bool = True                    

                if subunit == "5":
                    sub5_bool = True 

                if tma_bool and (sub2_bool or sub3_bool or sub5_bool) and FreqBand != None:
                    frq1tma = FreqBand.replace('17100','T')
                    frq1tma = frq1tma.replace('19200','M')
                    frq1tma = frq1tma.replace('25000','L')
                    frq1tma = frq1tma.replace('8800','D')
                    frq1tma = frq1tma.replace('8320','E')
                    frq1tma = frq1tma.replace('7030','J')
                    sub2_bool = False
                    if sub3_bool:
                        sub3_bool=False
                    if sub5_bool:
                        sub5_bool=False                        
                    salva = True

                if salva:
                    i = i + 1
                    salva = False
                    value1 = Scan(
                        request.user.id*1000+i,
                        bb1,
                        ldn_p[ldn_p.find('S')+1:ldn_p.find('-1')],
                        ldn_p[ldn_p.find('S')+1:ldn_p.find('-1')],
                        port_p,
                        type_p,
                        unique_id_p,
                        product_number_p,
                        str(frq1tma),
                        request.user.id,                
                    )
                    value1.save()
                    if salvaret:
                        salvaret = False
                        type_p = None

        except:
            ValueError()


        #+++++--- Estrazione seconda BB
        try:          
            scan_bb2 = ElementTree.parse(request.FILES['scan2'])
            path2 = str(request.FILES['scan2'])

            ldn_bool = True
            frq1tma = "--"
            tma_bool = False
            sub2_bool = False
            sub3_bool = False
            sub5_bool = False
            salva = False
            salvaret = False
            type = None
            unique_id = None
            product_number = None
            type_p = None                       
            unique_id_p = None
            product_number_p = None

            bb2 = path2[path2.find('=')+1:path2.find(',')]
            if len(bb2)>5:    
                bb2 = bb2[:bb2.find('_')]

            for node2 in scan_bb2.iter():

                ldn = node2.attrib.get('ldn')            
                if ldn == None:
                    ldn_bool = False
                else:
                    ldn_bool = True                
                if ldn_bool == True:
                    ldn_p = ldn
                    type_p = None
                    tma_bool = False

                port=node2.attrib.get('id')
                if port == 'A' or port == 'B' or port == 'C' or port == 'D' or port == 'R':
                    port_bool = True
                else:
                    port_bool = False                
                if port_bool == True:
                    port_p = port


                type=node2.attrib.get('type')
                if type != None:
                    type_p=node2.attrib.get('type')[-3:]                      
                    unique_id_p=node2.attrib.get('unique_id')
                    product_number_p=node2.attrib.get('product_number').rstrip()

                subunit=node2.attrib.get('subunit')
                FreqBand=node2.attrib.get('rxFreqBand')

                if type_p == "RET":
                    salvaret = True
                    salva = True
                    frq1tma = "--" 

                if type == "TMA":
                    tma_bool = True

                if subunit == "2":
                    sub2_bool = True

                if subunit == "3":
                    sub3_bool = True  

                if subunit == "5":
                    sub5_bool = True                      

                if tma_bool and (sub2_bool or sub3_bool or sub5_bool) and FreqBand != None:
                    frq1tma = FreqBand.replace('17100','T')
                    frq1tma = frq1tma.replace('19200','M')
                    frq1tma = frq1tma.replace('25000','L')
                    frq1tma = frq1tma.replace('8800','D')
                    frq1tma = frq1tma.replace('8320','E')
                    frq1tma = frq1tma.replace('7030','J')
                    sub2_bool = False
                    if sub3_bool:
                        sub3_bool=False
                    if sub5_bool:
                        sub5_bool=False                        
                    salva = True

                if salva:
                    i = i + 1
                    salva = False
                    value2 = Scan(
                        request.user.id*1000+i,
                        bb2,
                        ldn_p[ldn_p.find('S')+1:ldn_p.find('-1')],
                        ldn_p[ldn_p.find('S')+1:ldn_p.find('-1')],
                        port_p,
                        type_p,
                        unique_id_p,
                        product_number_p,
                        str(frq1tma),
                        request.user.id,                
                    )
                    value2.save()
                    if salvaret:
                        salvaret = False
                        type_p = None

        except:
            ValueError()
            

        return HttpResponseRedirect("/importa/scan-view2/")              
    
    #return render(request, 'import/import_scan.html')
    #return render(request, 'importa/import_scan_modal.html')
    #return render(request, 'importa/scan_view2.html')

    visualizza = True
    visualizzaelimina = False
    return render(request, 'importa/scan_view2.html', {'visualizza': visualizza, 'visualizzaelimina': visualizzaelimina}) 


def importValotiTma(request):
    if request.method == 'POST':
        tutto = ValoriTma.objects.all()
        tutto.delete()
        dataset = Dataset()
        valori = request.FILES['valoritma']
        imported_data = dataset.load(valori.read(), format = "xlsx")
        i = 0

        for data in imported_data:
            i = i + 1

            value = ValoriTma(
                i,
                data[0],
                data[1],
                data[2],
                data[3],
                data[4],
                data[5],
                data[6]                
           )
            value.save()            
                
        #return HttpResponseRedirect("/import/list-view/")              

    return render(request, 'importa/import_valoritma_modal.html')

def create_view(request):
    # dictionary for initial data with
    # field names as keys
    context ={}
 
    # add the dictionary during initialization
    form = AdprForm(request.POST or None)
    if form.is_valid():
        form.save()
        return HttpResponseRedirect("/importa/list-view/")
         
    context['form']= form
    return render(request, "importa/create_view.html", context)

def create_scan_view(request):
    # dictionary for initial data with
    # field names as keys
    context ={}
 
    # add the dictionary during initialization
    form = ScanForm(request.POST or None)
    if form.is_valid():
        form.save()
        return HttpResponseRedirect("/importa/scan-view/")
         
    context['form']= form
    return render(request, "importa/create_view.html", context)

def scan_view(request):
    # dictionary for initial data with
    # field names as keys
    context ={}
 
    # add the dictionary during initialization
    #context["dataset"] = Scan.objects.all()
    context["dataset"] = Scan.objects.filter(utente=request.user.id)
         
    return render(request, "importa/scan_view.html", context)

def scan_view2(request):
    RecordFormSet = modelformset_factory(Scan, formset=MyModelFormSet, 
                                         fields=('bb', 'radio', 'seq', 'port', 'type', "unique_id", 'product_number', 'freq1tma', 'utente'), 
                                         labels={'bb':'','radio':'','seq':'','port':'', 'type':'', 'unique_id':'', 'product_number':'', 'freq1tma':'', 'utente':''},                                                                                 
                                         can_delete=True, 
                                         extra=1, 
                                         widgets={'bb': TextInput(attrs={'size': '8'}),
                                                  'radio': TextInput(attrs={'size': '5'}),
                                                  'seq': TextInput(attrs={'size': '5'}),
                                                  'port': TextInput(attrs={'size': '5'}),
                                                  'type': TextInput(attrs={'size': '5'}), 
                                                  'unique_id': TextInput(attrs={'size': '30'}),
                                                  'product_number': TextInput(attrs={'size': '30'}),
                                                  'freq1tma': TextInput(attrs={'size': '5'}),
                                                  'utente': TextInput(attrs={'size': '5'}),		                                              
                                                },)
                                                           
    if request.method == 'POST':
        formset = RecordFormSet(request.POST, queryset=Scan.objects.filter(utente=request.user.id))

        if formset.is_valid():
            formset.save()   
                      
            return redirect('scan_view2')

    else:
        formset = RecordFormSet(queryset=Scan.objects.filter(utente=request.user.id))
      
    #return render(request, 'importa/scan_view2.html', {'formset': formset}) 


    visualizza = False
    visualizzaelimina = True
      
    return render(request, 'importa/scan_view2.html', {'formset': formset, 'visualizza': visualizza, 'visualizzaelimina': visualizzaelimina}) 



def list_view(request):
    # dictionary for initial data with
    # field names as keys
    context ={}
 
    # add the dictionary during initialization
    #context["dataset"] = Adpr.objects.all()
    context["dataset"] = Adpr.objects.filter(utente=request.user.id)
         
    return render(request, "importa/list_view.html", context)

def list_view2(request):
    RecordFormSet = modelformset_factory(Adpr, formset=MyModelFormSet, 
                                         fields=('cella', 'bb', 'seq', 'rusref', 'rutype', "layer", 'mxmod', 'mimo', 'tma', 'ret', 'tilt', 'utente'), 
                                         labels={'cella':'','bb':'','seq':'','rusref':'', 'rutype':'', 'layer':'', 'mxmod':'','mimo':'', 'tma':'', 'ret':'', 'tilt':'', 'utente':''},                                                                                 
                                         can_delete=True, 
                                         extra=1, 
                                         widgets={'cella': TextInput(attrs={'size': '8'}),
                                                  'bb': TextInput(attrs={'size': '7'}),
                                                  'seq': TextInput(attrs={'size': '10'}),
                                                  'rusref': TextInput(attrs={'size': '10'}),
                                                  'rutype': TextInput(attrs={'size': '10'}), 
                                                  'layer': TextInput(attrs={'size': '10'}),
                                                  'mxmod': TextInput(attrs={'size': '10'}),
                                                  'mimo': TextInput(attrs={'size': '10'}),
                                                  'tma': TextInput(attrs={'size': '10'}),
						                          'ret': TextInput(attrs={'size': '10'}),
						                          'tilt': TextInput(attrs={'size': '5'}),
                                                  'utente': TextInput(attrs={'size': '5'}),		                                              
                                                },)
                                                           
    if request.method == 'POST':
        formset = RecordFormSet(request.POST, queryset=Adpr.objects.filter(utente=request.user.id))
         
        if formset.is_valid():
            formset.save()   
                     
            return redirect('list_view2')
            

    else:
        formset = RecordFormSet(queryset=Adpr.objects.filter(utente=request.user.id))
   

    visualizza = False
    visualizzaelimina = True
      
    return render(request, 'importa/list_view2.html', {'formset': formset, 'visualizza': visualizza, 'visualizzaelimina': visualizzaelimina}) 

def detail_view(request, id):
    # dictionary for initial data with
    # field names as keys
    context ={}
 
    # add the dictionary during initialization
    context["data"] = Adpr.objects.get(id = id)
         
    return render(request, "importa/detail_view.html", context)    

def update_view(request, id):
    # dictionary for initial data with
    # field names as keys
    context ={}
 
    # fetch the object related to passed id
    obj = get_object_or_404(Adpr, id = id)
 
    # pass the object as instance in form
    form = AdprForm(request.POST or None, instance = obj)
 
    # save the data from the form and
    # redirect to detail_view
    if form.is_valid():
        form.save()
        #return HttpResponseRedirect("/import/"+id)
        return HttpResponseRedirect("/importa/list-view/")
 
    # add form dictionary to context
    context["form"] = form
 
    return render(request, "importa/update_view.html", context)    

def updateScan_view(request, id):
    # dictionary for initial data with
    # field names as keys
    context ={}
 
    # fetch the object related to passed id
    obj = get_object_or_404(Scan, id = id)
 
    # pass the object as instance in form
    form = ScanForm(request.POST or None, instance = obj)
 
    # save the data from the form and
    # redirect to detail_view
    if form.is_valid():
        form.save()
        #return HttpResponseRedirect("/import/"+id)
        return HttpResponseRedirect("/importa/scan-view/")
 
    # add form dictionary to context
    context["form"] = form
 
    return render(request, "importa/updateScan_view.html", context)    

def delete_view(request, id):
    # dictionary for initial data with
    # field names as keys
    context ={}
 
    # fetch the object related to passed id
    obj = get_object_or_404(Adpr, id = id)
 
    if request.method =="POST":
        # delete object
        obj.delete()
        # after deleting redirect to
        # home page
        return HttpResponseRedirect("/importa/list-view/")
 
    return render(request, "importa/delete_view.html", context)

def deletescan_view(request, id):
    # dictionary for initial data with
    # field names as keys
    context ={}
 
    # fetch the object related to passed id
    obj = get_object_or_404(Scan, id = id)
 
    if request.method =="POST":
        # delete object
        obj.delete()
        # after deleting redirect to
        # home page
        return HttpResponseRedirect("/importa/scan-view2/")
 
    return render(request, "importa/delete_view.html", context)

def deleteall_view(request):
    #tutto = Adpr.objects.all()
    tutto = Adpr.objects.filter(utente=request.user.id)
    tutto.delete()
    return HttpResponseRedirect("/importa/importa-adpr/")

def deleteallscan_view(request):
    #tutto = Scan.objects.all()
    tutto = Scan.objects.filter(utente=request.user.id)
    tutto.delete()

    return HttpResponseRedirect("/importa/importa-scan/")
 