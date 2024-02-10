from django.contrib import admin
from django.urls import path, include
from . import views

admin.site.site_header = "BlogWeb Admin"
admin.site.site_title = "BlogWeb Admin Panel"
admin.site.index_title = "BlogWeb Administration"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include("Home.urls")),
    path('blog/', include("Blog.urls")),
]
