from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.exceptions import PermissionDenied

class AdminRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.profile.role == 'Admin'

class EditorRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.profile.role == 'Editor'

class PembuatRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.profile.role == 'Pembuat'

class VerifikasiRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.profile.role in ['Admin', 'Editor']

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            raise PermissionDenied("You do not have permission to access this page.")
        return super().handle_no_permission()