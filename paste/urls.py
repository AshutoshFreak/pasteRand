from django.urls import path

from . import views
from .views import Detail, Index

app_name = "paste"

urlpatterns = [
    path("", view=Index.as_view(), name="index"),
    path("p/<str:slug>/", view=Detail.as_view(), name="detail"),
    path("post/<str:slug>/comment/", views.add_comment, name="add_comment"),
]
