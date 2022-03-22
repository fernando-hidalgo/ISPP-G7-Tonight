from django.contrib import admin
from django.urls import path
from proyecto import views
from django.contrib.auth.views import LoginView, LogoutView
from proyecto.views import ClientProfile, WelcomeClient, InicioVista, ErrorVista, BusinnessProfile, WelcomeBusiness
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', LoginView.as_view(template_name='login.html')),
    path('admin/', admin.site.urls),
    path('welcome_client/', WelcomeClient.as_view()),
    path('welcome_bussiness/', WelcomeBusiness.as_view()),
    path('inicio/', InicioVista.as_view()),
    path('cliente/<id>/', ClientProfile.as_view()),
    path('empresa/<id>/', BusinnessProfile.as_view()),
    path('cliente/', ErrorVista.as_view()),
    path('empresa/', ErrorVista.as_view()),
    path('error/', ErrorVista.as_view()),
    path('login/', LoginView.as_view(template_name='login.html')),
    path('logout/', LogoutView.as_view())
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
