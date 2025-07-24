from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Arsip
from django.core.mail import send_mail

@receiver(post_save, sender=Arsip)
def kirim_notifikasi_verifikasi(sender, instance, created, **kwargs):
    # Cek apakah status berubah menjadi diterima/ditolak
    if instance.tracker.has_changed('status_verifikasi') and instance.status_verifikasi in ['diterima', 'ditolak']:
        try:
            subject = f"Status Verifikasi Arsip: {instance.judul_arsip}"
            message = (
                f"Arsip Anda '{instance.judul_arsip}' telah {instance.get_status_verifikasi_display().lower()}.\n"
                f"Catatan: {instance.catatan_verifikasi or 'Tidak ada catatan tambahan'}\n\n"
                f"Terima kasih,\nTim Verifikasi"
            )
            send_mail(
                subject,
                message,
                'noreply@arsipdigital.com',
                [instance.dibuat_oleh.email],
                fail_silently=False,  # Ubah ke False untuk debug
            )
        except Exception as e:
            print(f"Gagal mengirim email: {e}")  # Log error
