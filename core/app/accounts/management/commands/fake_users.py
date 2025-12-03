from django.core.management.base import BaseCommand
from faker import Faker
import random
from app.accounts.models import User, Profile  # مسیر دقیق مدل‌ها

class Command(BaseCommand):
    help = "Generate fake users and profiles using Faker"

    def add_arguments(self, parser):
        parser.add_argument(
            "--total",
            type=int,
            default=10,
            help="Number of users to create"
        )

    def handle(self, *args, **options):
        total = options["total"]
        fake = Faker()

        for _ in range(total):
            email = fake.unique.email()
            password = "password123"  # می‌توانید تصادفی هم بسازید
            first_name = fake.first_name()
            last_name = fake.last_name()
            description = fake.text(max_nb_chars=200)

            # مقادیر تصادفی برای is_active و is_verified
            is_active = random.choice([True, False])
            is_verified = random.choice([True, False])

            user = User.objects.create_user(
                email=email,
                password=password,
                is_active=is_active,
                is_verified=is_verified
            )

            # پروفایل را آپدیت می‌کنیم
            profile = Profile.objects.get(user=user)
            profile.first_name = first_name
            profile.last_name = last_name
            profile.description = description
            profile.save()

            self.stdout.write(self.style.SUCCESS(
                f"Created user: {email} | active: {is_active} | verified: {is_verified}"
            ))


# Example usage: # python manage.py fake_users --total 20