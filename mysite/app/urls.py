from django.urls import path
from . import views
from django.views.generic.base import TemplateView

urlpatterns = [
    path('', views.search, name='search'),
    path('category/<slug>', views.search, name='search'),
    path('video/<slug>/', views.post_detail, name='post_detail'),
    path('about', views.about),
    path('privacy', views.privacy),
    path('terms', views.terms),
    path('contacts', views.contacts),
    path("sitemap.xml", views.sitemap),
    path(
        "robots.txt",
        TemplateView.as_view(template_name="robots.txt", content_type="text/plain"),
    ),

]
