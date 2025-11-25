from django.shortcuts import render, redirect
from .forms import SampleInputForm
from django.forms import modelformset_factory, formset_factory
from django.views import View
from .models import Tool

class ToolView(View):
    def get(self, request):

        table_rows = 10
        sample_form_set_factory = formset_factory(SampleInputForm, extra = table_rows)
        sample_form_set = sample_form_set_factory()

        context = {
            'sample_form' : sample_form_set,
        }
        return render(request, 'altro/tools.html', context)

    def post(self, request):

        sample_form_set_factory = formset_factory(SampleInputForm)
        formset = sample_form_set_factory(request.POST, queryset=Tool.objects.all())

        if formset.is_valid():
            formset.save()

        context = {
            'sample_form' : formset,
        }
        return render(request, 'altro/tools.html', context)



def view_tool(request):
                
    table_rows = 10
    sample_formset_factory = formset_factory(Tool,formset=SampleInputForm, extra = table_rows)
                                                        
    if request.method == 'POST':

        formset = sample_formset_factory(request.POST, Tool.objects.all())

        if formset.is_valid():
            formset.save()


            return redirect('ToolView')
    else:        
        formset = sample_formset_factory(Tool.objects.all())
        context = {'sample_form' : formset}
    
    
    return render(request, 'altro/tools.html', context)


