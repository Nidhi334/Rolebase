from .models import Permission, RolePermission

def has_permission(user, permission_name):
    """
    Check if the user has the specified permission based on their role.
    
    Args:
        user: CustomUser instance
        permission_name: String name of the permission (e.g., 'manage_billing')
    
    Returns:
        bool: True if the user has the permission, False otherwise
    """
    if not user.role:
        return False
    return user.role.rolepermission_set.filter(permission__name=permission_name).exists()