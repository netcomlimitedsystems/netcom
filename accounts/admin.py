from django.contrib import admin
from django.contrib.auth.models import User
from .models import Profile, AccountDeletionLog


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "avatar_preview", "bio")
    search_fields = ("user__username", "user__email")
    list_filter = ("user__date_joined",)

    def avatar_preview(self, obj):
        if obj.avatar:
            return f"✅ {obj.avatar.url}"
        return "❌ No Avatar"
    avatar_preview.short_description = "Avatar"


@admin.register(AccountDeletionLog)
class AccountDeletionLogAdmin(admin.ModelAdmin):
    list_display = ("user", "email", "reason", "deleted_at")
    search_fields = ("user", "email")
    list_filter = ("deleted_at",)
