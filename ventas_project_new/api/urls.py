from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token
from ventas.views import (ClienteViewSet,ProductoViewSet,VentaViewSet,DetalleVentaViewSet)
from django.urls import path

router = DefaultRouter()
router.register(r'clientes', ClienteViewSet)
router.register(r'productos', ProductoViewSet)
router.register(r'ventas', VentaViewSet)
router.register(r'detalle-ventas', DetalleVentaViewSet)

urlpatterns = [
    path('login/', obtain_auth_token),
]
urlpatterns += router.urls