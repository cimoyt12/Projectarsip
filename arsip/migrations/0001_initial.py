# Generated by Django 5.2.3 on 2025-07-10 16:50

import arsip.models
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Kategori',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nama', models.CharField(max_length=100, unique=True)),
                ('deskripsi', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nama', models.CharField(max_length=50, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.CharField(choices=[('Admin', 'Admin'), ('Editor', 'Editor'), ('Pembuat', 'Pembuat')], default='Pembuat', max_length=20)),
                ('email_verified', models.BooleanField(default=False)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Arsip',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('judul_arsip', models.CharField(blank=True, default='', max_length=255, null=True)),
                ('kode_arsip', models.CharField(blank=True, max_length=50, null=True, unique=True)),
                ('deskripsi', models.TextField(blank=True, default='', null=True)),
                ('tanggal_dibuat', models.DateField()),
                ('tanggal_diterima', models.DateField()),
                ('pembuat', models.CharField(blank=True, max_length=100, null=True)),
                ('lokasi_fisik', models.CharField(blank=True, max_length=100, null=True)),
                ('lokasi_digital', models.FileField(upload_to=arsip.models.arsip_upload_path)),
                ('format_file', models.CharField(blank=True, max_length=10)),
                ('ukuran_file', models.IntegerField(blank=True, null=True)),
                ('status_akses', models.CharField(choices=[('publik', 'Publik'), ('internal', 'Internal'), ('rahasia', 'Rahasia')], default='internal', max_length=20)),
                ('timestamp_input', models.DateTimeField(auto_now_add=True)),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('versi', models.PositiveIntegerField(default=1)),
                ('diakses', models.PositiveIntegerField(default=0)),
                ('status_verifikasi', models.CharField(choices=[('pending', 'Pending'), ('ditolak', 'Ditolak'), ('diterima', 'Diterima')], default='pending', max_length=20)),
                ('catatan_verifikasi', models.TextField(blank=True, null=True)),
                ('tanggal_verifikasi', models.DateTimeField(blank=True, null=True)),
                ('dibuat_oleh', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('verifikator', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='arsip_diverifikasi', to=settings.AUTH_USER_MODEL)),
                ('kategori', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='arsip.kategori')),
                ('tags', models.ManyToManyField(blank=True, to='arsip.tag')),
            ],
            options={
                'verbose_name': 'Arsip Digital',
                'verbose_name_plural': 'Arsip Digital',
                'ordering': ['-tanggal_diterima'],
            },
        ),
    ]
