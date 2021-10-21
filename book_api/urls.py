from django.urls import include, path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'Books', views.BooksViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('api-search/', views.SearchViewset, name = 'api_search'),
    path('api-auth/', include('rest_framework.urls',
        namespace='rest_framework'))
]