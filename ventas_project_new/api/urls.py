from rest_framework.routers import DefaultRouter
from ventas.views import (ClienteViewSet,ProductoViewSet,VentaViewSet)

router = DefaultRouter()
router.register(r'clientes', ClienteViewSet)
router.register(r'productos', ProductoViewSet)
router.register(r'ventas', VentaViewSet)

urlpatterns = router.urls