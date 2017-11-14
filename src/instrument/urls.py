#routerhez viewset regisrtálás
#urls.py globális url-ek közé (mmmk)

# from django.conf.urls import url
from rest_framework import routers


from . import apps
from . import views


router = routers.DefaultRouter(trailing_slash=False)
router.register(r'', views.InstrumentViewSet)

app_name = apps.InstrumentConfig.name
urlpatterns = router.urls
