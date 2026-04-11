from django.core.management.base import BaseCommand
from accounts.models import CTMSUser


class Command(BaseCommand):
    help = 'Seed initial user accounts for the CTMS platform'

    def handle(self, *args, **options):
        users = [
            {
                'username': 'admin',
                'email': 'admin@ctms.com',
                'password': 'Admin@123',
                'role': 'admin',
                'is_superuser': True,
                'is_staff': True,
                'first_name': 'System',
                'last_name': 'Administrator',
            },
            {
                'username': 'coordinator1',
                'email': 'coordinator1@ctms.com',
                'password': 'Coord@123',
                'role': 'coordinator',
                'is_superuser': False,
                'is_staff': False,
                'first_name': 'Sarah',
                'last_name': 'Mitchell',
            },
            {
                'username': 'coordinator2',
                'email': 'coordinator2@ctms.com',
                'password': 'Coord@123',
                'role': 'coordinator',
                'is_superuser': False,
                'is_staff': False,
                'first_name': 'James',
                'last_name': 'Thornton',
            },
        ]

        for user_data in users:
            password = user_data.pop('password')
            user, created = CTMSUser.objects.get_or_create(
                email=user_data['email'],
                defaults=user_data,
            )
            if created:
                user.set_password(password)
                user.save()
                self.stdout.write(
                    self.style.SUCCESS(f"Created user: {user.email} (role={user.role})")
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f"Already exists: {user.email} (role={user.role})")
                )

        self.stdout.write(self.style.SUCCESS('seed_users complete.'))
