from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from accounts.models import Profile

class Command(BaseCommand):
    help = "Create missing profiles for users that don't have one."

    def handle(self, *args, **kwargs):
        created_count = 0
        for user in User.objects.all():
            profile, created = Profile.objects.get_or_create(user=user)
            if created:
                created_count += 1
                self.stdout.write(self.style.SUCCESS(f"Created profile for user: {user.username}"))

        if created_count == 0:
            self.stdout.write(self.style.WARNING("No missing profiles found."))
        else:
            self.stdout.write(self.style.SUCCESS(f"✅ {created_count} profiles created successfully."))
