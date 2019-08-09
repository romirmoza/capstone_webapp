
from django.urls import path
from prelim import views

urlpatterns = [
            path('', views.prelim, name='prelim'),
            ]
