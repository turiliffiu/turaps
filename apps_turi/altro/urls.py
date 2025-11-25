from django.urls import path
from . import views


urlpatterns = [


    path("toolview/", 
          views.ToolView.as_view(), 
          name="ToolView"
     ),
    path("view-tool/", 
          views.view_tool, 
          name="view_tool"
     ),       

]


