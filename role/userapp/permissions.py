from rest_framework.permissions import Permission
from .utils import has_permission

def initialize_permissions():
    permissions = [
        'manage_billing', 'manage_patient', 'manage_doctor', 'manage_agent',
        'view_reports', 'manage_appointments', 'manage_lab_tests', 'manage_cc_billing',
        'manage_reception_cash', 'manage_clinical_master', 'manage_purchase',
        'manage_finance', 'view_dashboard', 'manage_marketing', 'manage_settings'
    ]
    for perm in permissions:
        Permission.objects.get_or_create(name=perm)

# Example usage of permissions
def has_permission(user, permission_name):
    if not user.role:
        return False
    return user.role.rolepermission_set.filter(permission__name=permission_name).exists()