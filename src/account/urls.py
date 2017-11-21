# from django.conf.urls import url
from rest_framework import routers


from . import apps
from . import views


router = routers.DefaultRouter(trailing_slash=False)
router.register(r'', views.ProfileViewSet)

#app_name = apps.AccountConfig.name
urlpatterns = router.urls
