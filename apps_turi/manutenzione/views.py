from django.shortcuts import render
from django.http import HttpResponseBadRequest, HttpResponseRedirect
from tablib import Dataset
from .models import TmplTma
from .tables import TmplTmaTable
from django.shortcuts import render, get_object_or_404





# Create your views here.

def importaTmplTma(request):
    if request.method == 'POST':
        tutto = TmplTma.objects.all()
        tutto.delete()
        dataset = Dataset()
        tmpltma = request.FILES['tmpltma']
        imported_data = dataset.load(tmpltma.read(), format = "xlsx")
        i = 0
        for data in imported_data:
            i = i + 1
            value = TmplTma(
                i,
                data[0],
                data[1],              
           )
            value.save()
                
        return HttpResponseRedirect("/importa/list-view/")

    return render(request, 'manutenzione/importa_tmpltma.html')


def listaTemplate(request):
    queryset = TmplTma.objects.all()
    table = TmplTmaTable(queryset)

    #table = TmplTmaTable(queryset, order_by=request.GET.get('sort'))

    return render(request, 'manutenzione/lista_template.html', {'table': table})


def dettaglio_template(request, id):
    template = get_object_or_404(TmplTma, pk=id)
    return render(request, 'manutenzione/dettaglio_template.html', {'template': template})

