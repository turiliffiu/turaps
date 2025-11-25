from django.urls import path

from django.contrib import admin
from django.urls import path
from core.views import home, login_view

from . import views

urlpatterns = [
    path("core/", views.HomeView.as_view(), name="homepage"),
    path("cerca/", views.cerca, name="funzione_cerca"),
    path("users/", views.UserList.as_view(), name="user_list"),
    path("user/<username>/", views.user_profile_view, name="user_profile"),
    path('admin/', admin.site.urls),

    path('', login_view, name='login_new'),
    path('home/', home, name='home'),    

]




