from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from PIL import Image
import os
from django.utils.timezone import now


def avatar_upload_path(instance, filename):
    """Dynamic path for avatar uploads."""
    base, ext = os.path.splitext(filename)
    return f"avatars/user_{instance.user.id}/{now().date()}_{base}{ext}"


class AccountDeletionLog(models.Model):
    user = models.CharField(max_length=150)  # store username instead of FK
    email = models.EmailField(null=True, blank=True)
    reason = models.TextField(blank=True, null=True)
    deleted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Deleted: {self.user} at {self.deleted_at.strftime('%Y-%m-%d %H:%M')}"


class Profile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="account_profile"  # ✅ important
    )
    avatar = models.ImageField(
        upload_to=avatar_upload_path,
        default="avatars/default.png",
        blank=True,
        null=True
    )
    bio = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"

    def save(self, *args, **kwargs):
        """Resize avatar if larger than 300x300."""
        super().save(*args, **kwargs)
        if self.avatar and hasattr(self.avatar, "path"):
            try:
                img = Image.open(self.avatar.path)
                if img.height > 300 or img.width > 300:
                    img.thumbnail((300, 300))
                    img.save(self.avatar.path)
            except Exception:
                # Ignore errors (e.g., when using in-memory storage like S3)
                pass


# ✅ Single clean signal
@receiver(post_save, sender=User)
def create_or_update_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    else:
        instance.account_profile.save()   # ✅ fixed
