from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()

class Command(BaseCommand):
    help = "Seed initial users for development."

    def handle(self, *args, **options):
        users =[
            {
                "email": "admin@example.com",
                "username": "admin",
                "password": "admin123",
                "is_staff": True,
                "is_superuser": True,
            },
            {
                "email": "user1@example.com",
                "username": "user1",
                "password": "password123",
            },
            {
                "email": "user2@example.com",
                "username": "user2",
                "password": "password123",
            },
        ]

        for data in users:
            if User.objects.filter(email=data["email"]).exists():
                self.stdout.write(
                    self.style.WARNING(f"User {data['email']} already exists")
                )
                continue

            user = User.objects.create_user(
                email=data["email"],
                username=data["username"],
                password=data["password"]
            )

            user.is_staff = data.get("is_staff", False)
            user.is_superuser = data.get("is_superuser", False)
            user.save()

            self.stdout.write(
                self.style.SUCCESS(f"Created user {data["email"]}")
            )
            