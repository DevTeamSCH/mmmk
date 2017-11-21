from rest_framework import routers

from . import views

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'', views.InstrumentViewSet)

# app_name = apps.InstrumentConfig.name
urlpatterns = router.urls
