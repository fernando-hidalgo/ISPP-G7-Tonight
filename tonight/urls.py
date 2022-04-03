from django.contrib import admin
from django.urls import path,include
from proyecto import views
from django.contrib.auth.views import LoginView, LogoutView
from django.conf import settings
from proyecto.views import ClientProfile, InicioVista, ErrorVista, BusinnessProfile, Entradas, WelcomeVista, ClientCreate, EmpresaCreate, EmpleadoCreate
from django.conf.urls.static import static

urlpatterns = [
    path('', WelcomeVista.as_view()),
    path('eventos/', views.listar_eventos, name='payment_done'),
    path('admin/', admin.site.urls),
    # path('welcome/', WelcomeVista.as_view()),
    path('crear_cliente/', ClientCreate.as_view()),
    path('inicio/', InicioVista.as_view()),
    path('cliente/<id>/', ClientProfile.as_view()),
    path('empresa/<id>/', BusinnessProfile.as_view()),
    path('cliente/', ErrorVista.as_view()),
    path('empresa/', ErrorVista.as_view()),
    path('error/', ErrorVista.as_view()),
    path('login/', LoginView.as_view(template_name='login.html')),
    path('logout/', LogoutView.as_view(template_name='welcome.html')),
    path('eventos/<int:evento_id>', views.ver_evento),
    path('eventos/<int:evento_id>/borrar', views.borrar_evento),
    path('eventos/<int:evento_id>/comprar', views.compra_directa),
    path('eventos/<int:evento_id>/vender', views.vender),
    path('eventos/<int:evento_id>/orden_comprar', views.orden_comprar),
    path('eventos/<pk>/editar', views.VistaEditarEvento.as_view()),
    path('eventos/crear', views.VistaCrearEvento.as_view()),
    path('eventos/<int:evento_id>/cancelar', views.cancelar_transaccion),
    path('eventos/<int:evento_id>/qr', views.QR),
    path('eventos/<int:evento_id>/scan', views.scan),
    path('empleados/<id>/', views.listar_eventos_empleado),
    path('crear_empresa/', EmpresaCreate.as_view()),
    #PAYPAL
    path('paypal/', include('paypal.standard.ipn.urls')),
    #Form view, where user inputs amount to recharge
    path('cliente/<id>/saldo', views.recargar_saldo),
    #Succes view
    path('saldo-exito/', views.payment_done, name='payment_done'),
    #Fail view
    path('saldo-cancelado/', views.payment_canceled, name='payment_cancelled'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)