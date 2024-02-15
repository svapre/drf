from .permissions import IsStaffEditorPermission
from rest_framework import permissions
from products.models import Product

class StaffEditorPermissionMixin():
    permission_classes = [permissions.IsAdminUser, IsStaffEditorPermission]

class UserQuerySetMixin():
    user_field = 'user'
    allow_sstaff_view = False
    
    def get_queryset(self, *args, **kwargs):
        user = self.request.user
        lookup_data = {}
        lookup_data[self.user_field] = user
        qs = super().get_queryset(*args, **kwargs)
        if self.allow_sstaff_view and user.is_staff:
            return qs
        return qs.filter(**lookup_data)