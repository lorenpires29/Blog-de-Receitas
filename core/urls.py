
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include ## adicionar include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('posts_app.urls')), # Adicionar isso.

]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) # Adicionar Isto
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) # Adicionar Isto