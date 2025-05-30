from django.urls import path
from django.views.generic.base import TemplateView
from django.contrib.auth import views as auth_views
from .views import home, administrar_productos, tienda, ficha
from .views import iniciar_sesion, registrar_usuario, cerrar_sesion
from .views import perfil_usuario, iniciar_pago, pago_exitoso, obtener_solicitudes_de_servicio
from .views import estado_solicitud, modificar_solicitud #agregado fernando
from .views import crear_solicitud, iniciar_pago_servicio, facturas   #agregado fernando



urlpatterns = [
    path('administrar_productos/<action>/<id>', administrar_productos, name="administrar_productos"),
    path('cambiar_password/', auth_views.PasswordChangeView.as_view(template_name='core/cambiar_password.html', success_url='/password_cambiada'), name='cambiar_password'),
    path('ficha/<id>', ficha, name="ficha"),
    path('', home, name="home"),
    path('iniciar_pago/<id>', iniciar_pago, name="iniciar_pago"),
    path('iniciar_sesion/', iniciar_sesion, name="iniciar_sesion"),
    path('obtener_solicitudes_de_servicio/', obtener_solicitudes_de_servicio, name="obtener_solicitudes_de_servicio"),
    path('pago_exitoso/', pago_exitoso, name="pago_exitoso"),
    path('password_cambiada/', TemplateView.as_view(template_name='core/password_cambiada.html'), name='password_cambiada'),
    path('perfil_usuario/', perfil_usuario, name="perfil_usuario"),
    path('registrar_usuario/', registrar_usuario, name="registrar_usuario"),
    path('tienda', tienda, name="tienda"),
    path('cerrar_sesion/', cerrar_sesion, name='cerrar_sesion'),
    path('solicitud/<int:nrosol>/<str:accion>/', estado_solicitud, name='estado_solicitud'), #agregado fernando
    path('solicitud/modificar/<int:nrosol>/', modificar_solicitud, name='modificar_solicitud'), #agregado fernando
    path('crear_solicitud/', crear_solicitud, name='crear_solicitud'), #agregado fernando
    path('iniciar_pago_servicio/', iniciar_pago_servicio, name='iniciar_pago_servicio'),#agregado fernando
    path('facturas/', facturas, name='facturas'), #agregado fernando

]