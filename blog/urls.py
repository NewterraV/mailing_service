from django.urls import path

from blog.apps import BlogConfig
from blog.views import BlogDetailView
from django.views.decorators.cache import cache_page


app_name = BlogConfig.name


urlpatterns = [
    path('detail/<int:pk>', cache_page(120)(BlogDetailView.as_view()), name='blog_detail')
]
