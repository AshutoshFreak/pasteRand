from django.urls import path

from .views import Detail, Index, comment_thread, raw_content

app_name = "paste"

urlpatterns = [
    path("", view=Index.as_view(), name="index"),
    path("p/<str:slug>/", view=Detail.as_view(), name="detail"),
    path("comment/<int:id>/", comment_thread, name="thread"),
    path("raw/<str:slug>/", raw_content, name="raw_content"),
]
