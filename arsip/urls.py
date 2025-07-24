from django.urls import path, include
from django.contrib.auth import views as auth_views
from rest_framework.routers import DefaultRouter
from .views import ArsipViewSet
from . import views
from .views import (
    VerifikasiArsipView, VerifikasiDetailView,
    dashboard, dashboard_pembuat, dashboard_editor
)

app_name = 'arsip'

urlpatterns = [
    path('', views.beranda, name='beranda'),
    path('api/arsip/', ArsipViewSet.as_view({'get': 'list', 'post': 'create'}), name='arsip-list'),
    path('api/arsip/<int:pk>/', ArsipViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='arsip-detail'),
    path('arsip/', views.daftar_arsip, name='daftar_arsip'),
    path('arsip/<int:arsip_id>/', views.detail_arsip, name='detail_arsip'),
    path('arsip/<int:arsip_id>/edit/', views.edit_arsip, name='edit_arsip'), # URL untuk edit
    path('arsip/<int:arsip_id>/hapus/', views.hapus_arsip, name='hapus_arsip'), # URL untuk hapus
    path('kategori/', views.kategori_list, name='kategori_list'),
    path('kategori/<int:kategori_id>/', views.arsip_per_kategori, name='arsip_per_kategori'),
    path('cari/', views.cari_arsip, name='cari_arsip'),
    path('upload/', views.upload_arsip, name='upload'),
    path('verifikasi/', VerifikasiArsipView.as_view(), name='verifikasi_arsip'),
    path('verifikasi/<int:pk>/', VerifikasiDetailView.as_view(), name='verifikasi_detail'),
    path('account/', dashboard, name='dashboard'),
    path('account/pembuat/', dashboard_pembuat, name='dashboard_pembuat'),
    path('account/editor/', dashboard_editor, name='dashboard_editor'),
    path('account/profil/', views.profil, name='profil'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='arsip/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='arsip:beranda'), name='logout'),
    path('password_change/<int:user_id>/', views.password_change, name='password_change'),
    path('password_reset/', views.password_reset_request, name='password_reset'),
    path('arsip/<int:arsip_id>/view/', views.view_digital_document, name='view_digital_document'),
    path('arsip/<int:arsip_id>/download/', views.download_digital_document, name='download_digital_document'),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
