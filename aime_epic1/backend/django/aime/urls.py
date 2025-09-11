from django.contrib import admin
from django.urls import path
from django.views.generic import RedirectView
from chat.views import chat_view, kb_search, home_view

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", home_view, name="home"),      # Home/landing
    path("chat/", chat_view, name="chat"),      # Chat page
    path("kb-search/", kb_search, name="kb_search"),
]
