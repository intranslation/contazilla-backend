from rest_framework.routers import DefaultRouter

from api.views.client import ClientsView


router = DefaultRouter()
router.register(r"clients", ClientsView, basename="client")

urlpatterns = router.urls
