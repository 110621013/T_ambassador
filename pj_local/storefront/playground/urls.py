from django.urls import path
from . import views

#URLConf
urlpatterns = [
    path('', views.product),
    path('path', views.path),
    path('map0',views.map0),
    path('map1',views.map1),
    path('map2',views.map2)
]
