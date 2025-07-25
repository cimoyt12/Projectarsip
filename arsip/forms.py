from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import SetPasswordForm
from .models import Arsip, Kategori # Import Kategori

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("Email already exists.")
        return email

class PasswordChangeForm(SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['new_password1'].help_text = "Enter a new password."
        self.fields['new_password2'].help_text = "Confirm the new password."

class ArsipForm(forms.ModelForm):
    # Buat lokasi_digital menjadi opsional secara default agar bisa ditangani di __init__
    # Django secara otomatis akan menambahkan 'Clear checkbox' jika initial data ada file.
    lokasi_digital = forms.FileField(label='Pilih File Arsip', required=False)

    class Meta:
        model = Arsip
        fields = [
            'judul_arsip',
            'deskripsi',
            'kategori',
            'tags',
            'tanggal_dibuat',
            'lokasi_digital', # Ditambahkan kembali di sini sebagai input field
            'status_akses',
            'pembuat',
        ]
        widgets = {
            'tanggal_dibuat': forms.DateInput(attrs={'type': 'date'}),
            'deskripsi': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Jika ini form edit (ada instance), maka file tidak wajib diisi ulang
        if self.instance and self.instance.pk:
            self.fields['lokasi_digital'].required = False
            self.fields['lokasi_digital'].label = 'Pilih File Arsip Baru (Opsional)'
        else:
            # Jika ini form upload baru, file wajib diisi
            self.fields['lokasi_digital'].required = True
            self.fields['lokasi_digital'].label = 'Pilih File Arsip'


class VerifikasiForm(forms.ModelForm):
    class Meta:
        model = Arsip
        fields = ['status_verifikasi', 'catatan_verifikasi']
        widgets = {
            'status_verifikasi': forms.RadioSelect,
            'catatan_verifikasi': forms.Textarea(attrs={'rows': 4}),
        }

# Form baru untuk Kategori
class KategoriForm(forms.ModelForm):
    class Meta:
        model = Kategori
        fields = ['nama', 'deskripsi']
        widgets = {
            'nama': forms.TextInput(attrs={'placeholder': 'Nama Kategori'}),
            'deskripsi': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Deskripsi Singkat Kategori'}),
        }
