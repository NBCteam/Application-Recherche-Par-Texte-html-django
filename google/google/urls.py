"""google URL Configuration

path('blog/', include('blog.urls'))

"""
from django.urls import include, path
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
    path(r'^/?$', 'google.searchengine.views.search'),
]
