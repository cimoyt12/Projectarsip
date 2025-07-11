from django import forms
from .models import Arsip

class ArsipForm(forms.ModelForm):
    class Meta:
        model = Arsip
        fields = ['judul_arsip', 'deskripsi', 'kategori', 'tags', 'tanggal_dibuat', 
                 'tanggal_diterima', 'pembuat', 'lokasi_fisik', 'lokasi_digital', 
                 'status_akses']
        widgets = {
            'tanggal_dibuat': forms.DateInput(attrs={'type': 'date'}),
            'tanggal_diterima': forms.DateInput(attrs={'type': 'date'}),
            'deskripsi': forms.Textarea(attrs={'rows': 3}),
        }

class VerifikasiForm(forms.ModelForm):
    class Meta:
        model = Arsip
        fields = ['status_verifikasi', 'catatan_verifikasi']
        widgets = {
            'status_verifikasi': forms.RadioSelect,
            'catatan_verifikasi': forms.Textarea(attrs={'rows': 4}),
        }