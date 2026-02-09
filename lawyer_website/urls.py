from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('lawyer_site.urls')),  # Подключаем URL приложения
]
