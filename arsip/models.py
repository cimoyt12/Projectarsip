from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver
from model_utils import FieldTracker
import os
import arsip

class Profile(models.Model):
    ROLE_CHOICES = (
        ('Admin', 'Admin'),
        ('Editor', 'Editor'),
        ('Pembuat', 'Pembuat'),
    )
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='Pembuat')
    email_verified = models.BooleanField(default=False)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if hasattr(instance, 'profile'):
        instance.profile.save()

# --- Fungsi untuk menentukan path upload ---
def arsip_upload_path(instance, filename):
    """Generate path based on received date: arsip/kategori/year/month_monthname/filename"""
    # Gunakan tanggal_diterima jika ada, jika tidak gunakan tanggal sekarang
    date = instance.tanggal_diterima if instance.tanggal_diterima else timezone.now().date()
    month_name = date.strftime("%B")
    
    # Ambil nama kategori, jika tidak ada gunakan "umum"
    kategori = instance.kategori.nama if instance.kategori else "umum"
    
    # Format: arsip/kategori/tahun/bulan_namabulan/filename
    return f"arsip/{kategori}/{date.year}/{date.month:02d}_{month_name}/{filename}"

class Kategori(models.Model):
    nama = models.CharField(max_length=100, unique=True)
    deskripsi = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return self.nama

class Tag(models.Model):
    nama = models.CharField(max_length=50, unique=True)
    
    def __str__(self):
        return self.nama

class Arsip(models.Model):
    STATUS_VERIFIKASI = (
        ('pending', 'Pending'),
        ('ditolak', 'Ditolak'),
        ('diterima', 'Diterima'),
    )

    STATUS_AKSES_CHOICES = [
        ('publik', 'Publik'),
        ('internal', 'Internal'),
    ]
    
    # Metadata utama
    judul_arsip = models.CharField(max_length=255, blank=True, null=True, default="")
    kode_arsip = models.CharField(max_length=50, blank=True, null=True, unique=True)
    deskripsi = models.TextField(blank=True, null=True, default="")
    
    # Klasifikasi
    kategori = models.ForeignKey(Kategori, on_delete=models.SET_NULL, blank=True, null=True)
    tags = models.ManyToManyField(Tag, blank=True)
    
    # Informasi tanggal
    tanggal_dibuat = models.DateField()
    tanggal_diterima = models.DateField()
    
    # Informasi pembuat dan lokasi
    pembuat = models.CharField(max_length=100, blank=True, null=True)
    lokasi_fisik = models.CharField(max_length=100, blank=True, null=True)
    
    # File digital - menggunakan fungsi arsip_upload_path
    lokasi_digital = models.FileField(upload_to=arsip_upload_path)
    format_file = models.CharField(max_length=10, blank=True)
    ukuran_file = models.IntegerField(blank=True, null=True)  # Dalam bytes
    
    # Kontrol akses dan audit
    status_akses = models.CharField(
        max_length=20, 
        choices=STATUS_AKSES_CHOICES, 
        default='internal'
    )
    dibuat_oleh = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    timestamp_input = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    
    # Metadata tambahan
    versi = models.PositiveIntegerField(default=1)
    diakses = models.PositiveIntegerField(default=0)
    
    def __str__(self):
        return self.judul_arsip
    
    def save(self, *args, **kwargs):
        """Otomatis isi format_file dan ukuran_file saat menyimpan"""
        if self.lokasi_digital:
            # Ambil ekstensi file
            self.format_file = os.path.splitext(self.lokasi_digital.name)[1][1:].upper()
            
            # Hitung ukuran file
            self.ukuran_file = self.lokasi_digital.size
        
        # Generate kode arsip otomatis jika belum ada
        if not self.kode_arsip:
            tahun = self.tanggal_diterima.year
            kategori_prefix = self.kategori.nama[:3].upper() if self.kategori else "GEN"
            last_record = Arsip.objects.filter(
                kategori=self.kategori,
                tanggal_diterima__year=tahun
            ).order_by('-id').first()
            
            seq = 1
            if last_record and last_record.kode_arsip:
                try:
                    last_seq = int(last_record.kode_arsip.split('-')[-1])
                    seq = last_seq + 1
                except (ValueError, IndexError):
                    pass
                    
            self.kode_arsip = f"{kategori_prefix}-{tahun}-{str(seq).zfill(3)}"
            
        super().save(*args, **kwargs)
    
    def get_ukuran_mb(self):
        """Mengembalikan ukuran file dalam MB dengan 2 desimal"""
        if self.ukuran_file:
            return round(self.ukuran_file / (1024 * 1024), 2)
        return 0
    
    class Meta:
        verbose_name = "Arsip Digital"
        verbose_name_plural = "Arsip Digital"
        ordering = ['-tanggal_diterima']

    status_verifikasi = models.CharField(
        max_length=20, 
        choices=STATUS_VERIFIKASI, 
        default='pending'
    )
    catatan_verifikasi = models.TextField(blank=True, null=True)
    verifikator = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='arsip_diverifikasi'
    )
    tanggal_verifikasi = models.DateTimeField(null=True, blank=True)
    tracker = FieldTracker(fields=['status_verifikasi'])
