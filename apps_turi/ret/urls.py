from django.urls import path
from . import views

urlpatterns = [

    
    path('edit-ret/', 
         views.edit_ret, 
         name='edit_ret'
         ),       
    path('view-ret/', 
         views.view_ret, 
         name='view_ret'
         ),
    path('view-ret2/', 
         views.view_ret2, 
         name='view_ret2'
         ),         
    path('delete-allret/', 
         views.delete_allret, 
         name='delete_allret'
         ),
    path('edit-cell/', 
         views.edit_cell, 
         name='edit_cell'
         ),
    path('edit-cell2/', 
         views.edit_cell2, 
         name='edit_cell2'
         ),  
    path('load-swapmatrix/', 
         views.load_swapmatrix, 
         name='load_swapmatrix'
         ),
    path('load-swapmatrix2/', 
         views.load_swapmatrix2, 
         name='load_swapmatrix2'
         ),
    path('crea-scrpit-ret/', 
         views.crea_scrpit_ret, 
         name='crea_scrpit_ret'
         ),  
    path("view-script-ret/", 
          views.view_script_ret, 
          name="view_script_ret"
          ),  
    path('modifica-script-ret/', 
          views.modifica_script_ret,
          name="modifica_script_ret" 
          ), 
    path("export-script1-ret/", 
          views.export_script1_ret, 
          name="export_script1_ret"
     ), 
    path("export-script2-ret/", 
          views.export_script2_ret, 
          name="export_script2_ret"
     ),    
    path("insert-serialtilt/", 
          views.insert_serialtilt, 
          name="insert_serialtilt"
     ), 
    path("view-swapmatrix/", 
          views.view_swapmatrix, 
          name="view_swapmatrix"
     ),

    path("view-swapmatrix2/", 
          views.view_swapmatrix2, 
          name="view_swapmatrix2"
     ),

    path('<id>/update-swapmatrix/', 
          views.update_swapmatrix,
          name="update_swapmatrix" 
     ),                                                                                                                     
]


