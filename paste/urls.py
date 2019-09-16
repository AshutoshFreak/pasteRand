from django.urls import path

from .views import CommentThread, Detail, Index, RawContent

app_name = "paste"

urlpatterns = [
    path("", Index.as_view(), name="index"),
    path("p/<str:slug>/", Detail.as_view(), name="detail"),
    path("comment/<int:id>/", CommentThread.as_view(), name="thread"),
    path("raw/<str:slug>/", RawContent.as_view(), name="raw_content"),
]
