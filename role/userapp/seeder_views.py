from django.core.management.base import BaseCommand
from userapp.models import Tenant, Role, Permission, RolePermission, Group, CustomUser
import uuid

class Command(BaseCommand):
    help = 'Seed the database with initial tenants, roles, permissions, groups, and users'

    def handle(self, *args, **kwargs):
        # Create Tenant
        tenant_id = uuid.UUID("123e4567-e89b-12d3-a456-426614174000")
        tenant, created = Tenant.objects.get_or_create(
            id=tenant_id, defaults={'name': 'Hospital A'}
        )
        self.stdout.write(self.style.SUCCESS(f'{"Created" if created else "Found"} tenant: {tenant.name}'))

        # Create Permissions
        permissions_data = [
            {'name': 'manage_billing', 'description': 'Can manage billing operations'},
            {'name': 'manage_patient', 'description': 'Can manage patient records'},
            {'name': 'manage_doctor', 'description': 'Can manage doctor records'},
            {'name': 'manage_agent', 'description': 'Can manage agent records'},
            {'name': 'view_reports', 'description': 'Can view reports'},
            {'name': 'manage_appointments', 'description': 'Can manage appointments'},
            {'name': 'manage_lab_tests', 'description': 'Can manage lab tests'},
            {'name': 'manage_cc_billing', 'description': 'Can manage CC billing'},
            {'name': 'manage_reception_cash', 'description': 'Can manage reception cash'},
            {'name': 'manage_clinical_master', 'description': 'Can manage clinical master data'},
            {'name': 'manage_purchase', 'description': 'Can manage purchases'},
            {'name': 'manage_finance', 'description': 'Can manage finance operations'},
            {'name': 'view_dashboard', 'description': 'Can view dashboard'},
            {'name': 'manage_marketing', 'description': 'Can manage marketing'},
            {'name': 'manage_settings', 'description': 'Can manage settings'},
        ]
        for perm_data in permissions_data:
            Permission.objects.get_or_create(name=perm_data['name'], defaults={'description': perm_data['description']})
            self.stdout.write(self.style.SUCCESS(f'Created or found permission: {perm_data["name"]}'))

        # Create Roles
        roles_data = [
            {'name': 'Front Desk', 'description': 'Handles front desk operations', 'permissions': ['manage_billing', 'manage_appointments', 'manage_reception_cash']},
            {'name': 'Lab Desk', 'description': 'Handles lab operations', 'permissions': ['manage_lab_tests', 'manage_clinical_master']},
            {'name': 'Account Desk', 'description': 'Handles account operations', 'permissions': ['manage_purchase', 'manage_finance']},
            {'name': 'Admin', 'description': 'Full administrative access', 'permissions': permissions_data}
        ]
        for role_data in roles_data:
            role, created = Role.objects.get_or_create(
                name=role_data['name'], tenant_id=tenant, defaults={'description': role_data['description']}
            )
            self.stdout.write(self.style.SUCCESS(f'{"Created" if created else "Found"} role: {role.name}'))

            # Assign Permissions to Role
            for perm_name in role_data['permissions']:
                permission = Permission.objects.get(name=perm_name)
                RolePermission.objects.get_or_create(role=role, permission=permission)
                self.stdout.write(self.style.SUCCESS(f'Assigned permission {perm_name} to role {role.name}'))

        # Create Groups
        groups_data = [
            {'name': 'Billing Team', 'roles': ['Front Desk']},
            {'name': 'Reception Team', 'roles': ['Front Desk']},
            {'name': 'Lab Team', 'roles': ['Lab Desk']},
            {'name': 'Account Team', 'roles': ['Account Desk']}
        ]
        for group_data in groups_data:
            group, created = Group.objects.get_or_create(name=group_data['name'], tenant_id=tenant)
            self.stdout.write(self.style.SUCCESS(f'{"Created" if created else "Found"} group: {group.name}'))

            # Assign Roles to Group
            for role_name in group_data['roles']:
                role = Role.objects.get(name=role_name, tenant_id=tenant)
                group.roles.add(role)
                self.stdout.write(self.style.SUCCESS(f'Assigned role {role_name} to group {group.name}'))

        # Create Users
        users_data = [
            {
                'email': 'user@example.com',
                'password': 'securepassword123',
                'first_name': 'John',
                'last_name': 'Doe',
                'role': 'Front Desk',
                'groups': ['Billing Team', 'Reception Team']
            },
            {
                'email': 'labuser@example.com',
                'password': 'securepassword123',
                'first_name': 'Jane',
                'last_name': 'Smith',
                'role': 'Lab Desk',
                'groups': ['Lab Team']
            },
            {
                'email': 'admin@example.com',
                'password': 'securepassword123',
                'first_name': 'Admin',
                'last_name': 'User',
                'role': 'Admin',
                'groups': []
            }
        ]
        for user_data in users_data:
            user, created = CustomUser.objects.get_or_create(
                email=user_data['email'],
                defaults={
                    'first_name': user_data['first_name'],
                    'last_name': user_data['last_name'],
                    'tenant_id': tenant,
                    'role': Role.objects.get(name=user_data['role'], tenant_id=tenant)
                }
            )
            if created:
                user.set_password(user_data['password'])
                user.save()
                self.stdout.write(self.style.SUCCESS(f'Created user: {user.email}'))
            else:
                self.stdout.write(self.style.WARNING(f'User already exists: {user.email}'))

            # Assign Groups to User
            for group_name in user_data['groups']:
                group = Group.objects.get(name=group_name, tenant_id=tenant)
                group.users.add(user)
                self.stdout.write(self.style.SUCCESS(f'Assigned user {user.email} to group {group_name}'))