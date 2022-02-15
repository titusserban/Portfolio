from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from homepage.views import HomePage

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", HomePage.as_view(), name="homepage"),
    path("googleapi/", include("googleapi.urls")),
    path("openweatherapi/", include("openweatherapi.urls")),
    path("registration/", include("registration.urls")),
    path("datascience/", include("datascience.urls")),
] 

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
