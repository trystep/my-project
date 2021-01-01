from django.urls import path, re_path
from . import views
from django.views.generic.base import TemplateView

urlpatterns = [
    path('', views.search, name='search'),
    path('category/<slug>', views.search, name='search'),
    path('video/<slug>/', views.post_detail, name='post_detail'),
    # Эта строка требуется для отображения карты сайта по адресу .../sitemap.xml
    path(
        "sitemap.xml",
        TemplateView.as_view(template_name="sitemap.xml", content_type="text/xml"),
    ),
    # Эта строка требуется для стилизации карты сайта sitemap, чтобы можно было переходить по ссылке из карты
    # сайта. По адресу /sitemap.xsl находятся стили для sitemap.xml
    path(
        "sitemap.xsl",
        TemplateView.as_view(template_name="sitemap.xsl", content_type="text/xsl"),
    ),
    # Эта строка требуется для отображения robots.txt по адресу .../robots.txt
    path(
        "robots.txt",
        TemplateView.as_view(template_name="robots.txt", content_type="text/plain"),
    ),

]
