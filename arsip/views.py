from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView
from django.utils import timezone
from .models import Arsip, Kategori
from .forms import ArsipForm, VerifikasiForm
from django.core.paginator import Paginator
from django.db.models import Count, Q
from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from .serializers import ArsipSerializer
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .permissions import PembuatRequiredMixin, VerifikasiRequiredMixin
from .forms import ArsipForm
from django.contrib import messages

@login_required
def dashboard(request):
    profile = request.user.profile
    
    if profile.role == 'admin':
        return redirect('dashboard_admin')
    elif profile.role == 'editor':
        return redirect('dashboard_editor')
    elif profile.role == 'pembuat':
        return redirect('dashboard_pembuat')
    else:
        return redirect('beranda')

@login_required
def dashboard_pembuat(request):
    if request.user.profile.role != 'pembuat':
        return redirect('beranda')
    
    arsip_pribadi = Arsip.objects.filter(
        dibuat_oleh=request.user
    ).order_by('-tanggal_diterima')
    
    return render(request, 'arsip/dashboard_pembuat.html', {
        'arsip_pribadi': arsip_pribadi
    })

@login_required
def dashboard_editor(request):
    if request.user.profile.role not in ['admin', 'editor']:
        return redirect('beranda')
    
    arsip_pending = Arsip.objects.filter(status_verifikasi='pending').count()
    arsip_diverifikasi = Arsip.objects.filter(
        verifikator=request.user
    ).order_by('-tanggal_verifikasi')[:5]
    
    return render(request, 'arsip/dashboard_editor.html', {
        'arsip_pending': arsip_pending,
        'arsip_diverifikasi': arsip_diverifikasi
    })

class ArsipViewSet(viewsets.ModelViewSet):
    queryset = Arsip.objects.all()
    serializer_class = ArsipSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['kategori', 'status_akses']

def beranda(request):
    arsip_terbaru = Arsip.objects.filter(
        status_verifikasi='diterima'
    ).order_by('-tanggal_diterima')[:6]
    kategori_populer = Kategori.objects.annotate(
        jumlah_arsip=Count('arsip')
    ).order_by('-jumlah_arsip')[:5]

    return render(request, 'arsip/beranda.html', {
        'arsip_terbaru': arsip_terbaru,
        'kategori_populer': kategori_populer,
    })

def daftar_arsip(request):
    arsip_list = Arsip.objects.filter(status_verifikasi='diterima')
    kategori_id = request.GET.get('kategori')
    status_akses = request.GET.get('status_akses')

    if kategori_id:
        arsip_list = arsip_list.filter(kategori_id=kategori_id)
    if status_akses:
        arsip_list = arsip_list.filter(status_akses=status_akses)

    arsip_list = arsip_list.order_by('-tanggal_diterima')
    paginator = Paginator(arsip_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    kategori_list = Kategori.objects.all().order_by('nama')

    return render(request, 'arsip/daftar_arsip.html', {
        'page_obj': page_obj,
        'kategori_list': kategori_list,
    })

def detail_arsip(request, arsip_id):
    arsip = Arsip.objects.get(id=arsip_id)
    arsip.diakses += 1
    arsip.save()
    
    arsip_terkait = Arsip.objects.filter(
        kategori=arsip.kategori
    ).exclude(id=arsip.id).order_by('-tanggal_diterima')[:3]

    # Tambahkan URL absolut untuk file arsip (jika ada)
    arsip_url_absolute = request.build_absolute_uri(arsip.lokasi_digital.url) if arsip.lokasi_digital else ''
    
    return render(request, 'arsip/detail_arsip.html', {
        'arsip': arsip,
        'arsip_terkait': arsip_terkait,
        'arsip_url_absolute': arsip_url_absolute,
    })

def kategori_populer(request):
    kategori_populer = Kategori.objects.annotate(
        jumlah_arsip=Count('arsip')
    ).order_by('-jumlah_arsip')[:4]
    
    return render(request, 'arsip/kategori_populer.html', {
        'kategori_populer': kategori_populer
    })

def kategori_list(request):
    kategori = Kategori.objects.all().annotate(
        jumlah_arsip=Count('arsip')
    ).order_by('nama')
    return render(request, 'arsip/kategori_list.html', {
        'kategori_list': kategori
    })

def arsip_per_kategori(request, kategori_id):
    kategori = Kategori.objects.get(id=kategori_id)
    # Ganti tanggal_upload dengan tanggal_diterima
    arsip_list = Arsip.objects.filter(kategori=kategori).order_by('-tanggal_diterima')
    return render(request, 'arsip/arsip_per_kategori.html', {
        'kategori': kategori,
        'arsip_list': arsip_list
    })

def cari_arsip(request):
    query = request.GET.get('q', '')
    # Ganti judul menjadi judul_arsip dan tanggal_upload dengan tanggal_diterima
    results = Arsip.objects.filter(
        Q(judul_arsip__icontains=query) | 
        Q(deskripsi__icontains=query) |
        Q(kategori__nama__icontains=query)
    ).order_by('-tanggal_diterima')
    
    return render(request, 'arsip/hasil_pencarian.html', {
        'query': query,
        'results': results
    })

class UploadArsipView(LoginRequiredMixin, PembuatRequiredMixin, CreateView):
    model = Arsip
    form_class = ArsipForm
    template_name = 'arsip/upload.html'
    success_url = reverse_lazy('daftar_arsip_pribadi')
    
    def form_valid(self, form):
        form.instance.dibuat_oleh = self.request.user
        form.instance.status_verifikasi = 'pending'
        return super().form_valid(form)
    
class VerifikasiArsipView(LoginRequiredMixin, VerifikasiRequiredMixin, ListView):
    model = Arsip
    template_name = 'arsip/verifikasi_list.html'
    context_object_name = 'arsip_list'
    
    def get_queryset(self):
        return Arsip.objects.filter(status_verifikasi='pending')

class VerifikasiDetailView(LoginRequiredMixin, VerifikasiRequiredMixin, UpdateView):
    model = Arsip
    form_class = VerifikasiForm
    template_name = 'arsip/verifikasi_detail.html'
    success_url = reverse_lazy('arsip:verifikasi_arsip')
    
    def form_valid(self, form):
        form.instance.verifikator = self.request.user
        form.instance.tanggal_verifikasi = timezone.now()
        return super().form_valid(form)

@login_required
def profil(request):
    return render(request, 'arsip/profil.html', {
        'user': request.user,
        'profile': request.user.profile,
    })

def statistik_context(request):
    from .models import Arsip, Kategori
    return {
        'total_arsip': Arsip.objects.count(),
        'total_kategori': Kategori.objects.count(),
    }

@login_required
def upload_arsip(request):
    if request.user.username not in ['admin1', 'editor1']:
        messages.error(request, 'Anda tidak memiliki izin untuk mengupload arsip.')
        return redirect('arsip:daftar_arsip')
    if request.method == 'POST':
        form = ArsipForm(request.POST, request.FILES)
        if form.is_valid():
            arsip = form.save(commit=False)
            arsip.dibuat_oleh = request.user
            arsip.save()
            form.save_m2m()
            messages.success(request, 'Arsip berhasil diupload.')
            return redirect('arsip:daftar_arsip')
    else:
        form = ArsipForm()
    return render(request, 'arsip/upload.html', {'form': form})