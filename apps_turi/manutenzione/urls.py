from django.urls import path
from . import views

urlpatterns = [
        path('importa-tmpltma/', 
            views.importaTmplTma, 
            name="importa_tmpltma"
        ),   
        path('lista-template/', 
            views.listaTemplate, 
            name="lista_template"
        ),
        path('<id>/dettaglio-template/', 
            views.dettaglio_template, 
            name="dettaglio_template"
        ),          
]