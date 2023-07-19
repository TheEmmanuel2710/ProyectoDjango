from django.urls import re_path
from . import views

urlpatterns = [
    re_path(r'^categoria$',views.CategoriaList.as_view()),
    re_path(r'^categoria/(?P<pk>[0-9]+)$',views.CategoriaDetail.as_view()),
    re_path(r'^producto$',views.ProductoList.as_view()),
    re_path(r'^categoria/(?P<pk>[0-9]+)$',views.ProductoDetail.as_view()),
]