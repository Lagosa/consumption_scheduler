from django.urls import path

from . import views
from .Controllers import APIEndpoints

urlpatterns = [
    path("", views.index, name="index"),
    path("hello/", APIEndpoints.getData),
    path("initial_consumption/", APIEndpoints.initial_consumption),
    path("save_dataset", APIEndpoints.save_dataset),
    path("datasets", APIEndpoints.get_datasets),
    path("evaluate", APIEndpoints.evaluate),
    path("operationCodes", APIEndpoints.get_operationCodes),
    path("solution_file", APIEndpoints.get_solutionFile)
]
