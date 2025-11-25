from django.urls import path
from . import views

urlpatterns = [
    path("view-script-gsm/", 
          views.view_script_gsm, 
          name="view_script_gsm"
          ),  

    path('crea-script-gsm/', 
          views.crea_script_gsm, 
          name='crea_script_gsm'
          ),  
    path('modifica-script-gsm/', 
          views.modifica_script_gsm,
          name="modifica_script_gsm" 
          ), 
    path("export-script-gsm/", 
          views.export_script_gsm, 
          name="export_script_gsm"
     ),                     
]