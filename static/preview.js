// File: static/js/preview.js
document.addEventListener('DOMContentLoaded', function() {
  const previewModal = new bootstrap.Modal('#previewModal',{
    backdrop: 'static',
    keyboard: false
  });

  // Inisialisasi modal
  const modal = new bootstrap.Modal(previewModal, {
    backdrop: 'static',  // Mencegah modal tertutup saat klik di luar
    keyboard: false      // Mencegah modal tertutup dengan tombol ESC
  });

  // Handler untuk tombol preview
  document.querySelector('[data-bs-target="#previewModal"]').addEventListener('click', function(e) {
    e.preventDefault();
    
    // Tampilkan loading spinner
    const container = document.getElementById('preview-content');
    container.innerHTML = `
      <div class="text-center py-5">
        <div class="spinner-border text-primary" role="status">
          <span class="visually-hidden">Loading...</span>
        </div>
        <p>Memuat pratinjau...</p>
      </div>
    `;

    setTimeout(() => {
        container.innerHTML = `{% include "arsip/_preview_content.html" %}`;
    }, 1000); // Simulasi delay 1 detik untuk loading
    
    // Tampilkan modal
    previewModal.show();
  });

  // Bersihkan konten saat modal ditutup
  previewModal.addEventListener('hidden.bs.modal', function() {
    document.getElementById('preview-content').innerHTML = '';
  });
});