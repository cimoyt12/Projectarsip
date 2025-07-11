from django.contrib import admin
from .models import Arsip, Kategori, Tag, Profile


class ArsipAdmin(admin.ModelAdmin):
    list_display = ('judul_arsip', 'kategori', 'status_akses', 'tanggal_diterima', 'dibuat_oleh')
    list_filter = ('status_akses', 'kategori', 'tags')
    search_fields = ('judul_arsip', 'deskripsi', 'kode_arsip')
    readonly_fields = ('format_file', 'ukuran_file', 'timestamp_input', 'last_updated')
    date_hierarchy = 'tanggal_diterima'
    fieldsets = (
        ('Metadata Utama', {
            'fields': ('judul_arsip', 'kode_arsip', 'deskripsi')
        }),
        ('Klasifikasi', {
            'fields': ('kategori', 'tags')
        }),
        ('Informasi Tanggal', {
            'fields': ('tanggal_dibuat', 'tanggal_diterima')
        }),
        ('Informasi File', {
            'fields': ('lokasi_digital', 'format_file', 'ukuran_file')
        }),
        ('Kontrol Akses', {
            'fields': ('status_akses', 'dibuat_oleh')
        }),
        ('Audit Trail', {
            'fields': ('timestamp_input', 'last_updated', 'diakses'),
            'classes': ('collapse',)
        }),
    )

admin.site.register(Arsip, ArsipAdmin)
admin.site.register(Kategori)
admin.site.register(Tag)
admin.site.register(Profile)