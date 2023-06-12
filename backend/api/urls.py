from django.urls import include, path

from rest_framework.routers import DefaultRouter

from .views import CityViewSet, find_ticket


app_name = 'api'

router = DefaultRouter()

router.register('cities', CityViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('airline', find_ticket, name='airline')
]
