from django.urls import path
from . import views 


urlpatterns = [
path('simulation/', views.simulation, name='simulation')
]