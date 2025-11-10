from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from .views import NaturalPersonListView, NaturalPersonCreateView, NaturalPersonDetailView, NaturalPersonUpdateView, NaturalPersonReportsView
from . import views

urlpatterns = [
    path('', views.home, name='home-person'),
    path('choice/', views.choice_person, name='person-choice'),
    path('natural/', NaturalPersonListView.as_view(), name='natural-list'),
    path('natural/create', NaturalPersonCreateView.as_view(), name='natural-create'),
    path('natural/reports', NaturalPersonReportsView.as_view(), name='natural-reports'),
    path('natural/<int:pk>', NaturalPersonDetailView.as_view(), name='natural-detail'),
    path('natural/<int:pk>/edit', NaturalPersonUpdateView.as_view(), name='natural-update'),
] 

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)