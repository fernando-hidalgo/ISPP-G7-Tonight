from django.contrib import admin
from django.urls import path,include
from proyecto import views
from django.contrib.auth.views import LoginView, LogoutView
from django.conf import settings
from proyecto.views import ClientProfile, InicioVista, VistaEditarEvento, ErrorVista, BusinnessProfile, Entradas, WelcomeVista, ClientCreate, EmpresaCreate, EmpleadoCreate, TerminosVista
from django.conf.urls.static import static

urlpatterns = [
    path('paypal/', include('paypal.standard.ipn.urls')),
    
    #Accesibles SOLO para Clientes
    path('eventosmapa/', views.mapa_eventos),
    path('eventos/', views.listar_eventos, name='payment_done'),
    path('cliente/<id>/', ClientProfile.as_view()),
    path('cliente/<id>/saldo', views.recargar_saldo),
    path('saldo-exito/', views.payment_done, name='payment_done'),
    path('saldo-cancelado/', views.payment_canceled, name='payment_cancelled'),
    path('eventos/<int:evento_id>/comprar', views.compra_directa),
    path('eventos/<int:evento_id>/vender', views.vender),
    path('eventos/<int:evento_id>/orden_comprar', views.orden_comprar),
    path('eventos/<int:evento_id>/cancelar', views.cancelar_transaccion),
    path('eventos/<int:evento_id>/qr', views.QR),
    
    #Accesible SOLO para Empresas
    path('empresa/<id>/', BusinnessProfile.as_view()),
    path('eventos/<int:evento_id>/borrar', views.borrar_evento),
    path('eventos/<pk>/editar', VistaEditarEvento.as_view()),
    path('eventos/crear', views.crear_fiesta),
    path('empleados/crear', EmpleadoCreate.as_view()),
    
    #Accesible por Empleado
    path('eventos/<int:evento_id>/scan', views.scan),
    path('empleados/<id>/', views.listar_eventos_empleado),
    
    #Accesible por Cliente, Empleado y Empresa
    path('eventos/<int:evento_id>', views.ver_evento),
    
    #Accesible sin Login
    path('', WelcomeVista.as_view()),
    path('admin/', admin.site.urls),
    path('inicio/', InicioVista.as_view()),
    path('error/', ErrorVista.as_view()),
    path('login/', LoginView.as_view(template_name='login.html')),
    path('logout/', LogoutView.as_view(template_name='welcome.html')),
    path('crear_empresa/', EmpresaCreate.as_view()),
    path('crear_cliente/', ClientCreate.as_view()),
    path('terminos/', TerminosVista.as_view()),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)