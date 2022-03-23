from django.contrib import admin
from django.urls import path
from proyecto import views
from django.contrib.auth.views import LoginView, LogoutView
from proyecto.views import ClientProfile, WelcomeClient, InicioVista, ErrorVista, BusinnessProfile, WelcomeBusiness, Entradas
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', LoginView.as_view(template_name='login.html')),
    path('eventos/', views.listar_eventos),
    path('admin/', admin.site.urls),
    path('welcome_client/', WelcomeClient.as_view()),
    path('welcome_bussiness/', WelcomeBusiness.as_view()),
    path('inicio/', InicioVista.as_view()),
    path('cliente/<id>/', ClientProfile.as_view()),
    path('empresa/<id>/', BusinnessProfile.as_view()),
    path('cliente/', ErrorVista.as_view()),
    path('empresa/', ErrorVista.as_view()),
    path('error/', ErrorVista.as_view()),
    path('entrada/<id>/',Entradas.as_view()),
    #path('entrada/<id>/vender/',Entradas.vender),
    path('login/', LoginView.as_view(template_name='login.html')),
    path('logout/', LogoutView.as_view()),

    path('qr', views.QR),
    path('scan', views.scan)

    path('eventos/<int:evento_id>', views.ver_evento),
    path('eventos/<int:evento_id>/borrar', views.borrar_evento),
    path('eventos/<pk>/editar', views.VistaEditarEvento.as_view()),
    path('eventos/crear', views.VistaCrearEvento.as_view()),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
