from django.urls import path

from .views import Detail, Index, comment_thread

app_name = "paste"

urlpatterns = [
    path("", view=Index.as_view(), name="index"),
    path("p/<str:slug>/", view=Detail.as_view(), name="detail"),
    path("comment/<int:id>/", comment_thread, name="thread"),
]
