from django.urls import path
from . import views

app_name = "quotes"

urlpatterns = [
    path("", views.main, name="root"),
    path("<int:page>", views.main, name="root_paginate"),
    path("author/<str:author_id>", views.author_detail, name="author_detail"),
    path("add_author/", views.AddAuthorView.as_view(), name="add_author"),
    path("add_quote/", views.AddQuoteView.as_view(), name="add_quote"),
]
