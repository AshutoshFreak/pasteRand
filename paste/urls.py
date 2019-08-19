from django.urls import path

from . import views

app_name = "paste"

urlpatterns = [
    path("", views.index, name="index"),
    path("p/<str:slug>/", views.detail, name="detail"),
]
