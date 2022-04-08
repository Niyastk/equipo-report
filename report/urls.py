

from django.urls import path
from . import views
urlpatterns = [
    path('', views.report_generator, name='generate_report'),
]
