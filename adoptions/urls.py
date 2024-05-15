from django.urls import path, include
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path("", views.petFest, name="index"),
    path('load_pets/', login_required(views.load_pets), name='load_pets'),
    path('pet/<int:pet_id>/', login_required(views.pet_detail_view), name='pet_detail'),
    path('pet/<int:pet_id>/hold/', login_required(views.pet_hold_view), name='pet_hold'),
    path('accounts/', include('django.contrib.auth.urls')),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)