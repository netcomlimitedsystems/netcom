# admin.py
from django.contrib import admin
from django.contrib.auth.models import User
from django.db.models import Count
from django.utils.timezone import now, timedelta

from courses.models import Course, Lesson, Enrollment, Blog
from accounts.models import Profile, AccountDeletionLog


class CustomAdminSite(admin.AdminSite):
    site_header = "Netcom Admin"
    site_title = "Netcom Admin Portal"
    index_title = "Welcome to the Admin Dashboard"

    def index(self, request, extra_context=None):
        today = now().date()
        last_week = today - timedelta(days=6)  # past 7 days including today

        # Stats
        users_count = User.objects.count()
        courses_count = Course.objects.count()
        enrollments_count = Enrollment.objects.count()
        blogs_count = Blog.objects.count()
        deletions_count = AccountDeletionLog.objects.count()

        # --- User Growth (last 7 days) ---
        user_growth = (
            User.objects.filter(date_joined__date__gte=last_week)
            .extra(select={"day": "date(date_joined)"})
            .values("day")
            .annotate(count=Count("id"))
            .order_by("day")
        )
        user_growth_dict = {str(u["day"]): u["count"] for u in user_growth}

        user_growth_labels = [
            str((last_week + timedelta(days=i))) for i in range(7)
        ]
        user_growth_data = [user_growth_dict.get(day, 0) for day in user_growth_labels]

        # --- Enrollment Growth (last 7 days) ---
        enrollment_growth = (
            Enrollment.objects.filter(enrolled_at__date__gte=last_week)
            .extra(select={"day": "date(enrolled_at)"})
            .values("day")
            .annotate(count=Count("id"))
            .order_by("day")
        )
        enrollment_growth_dict = {str(e["day"]): e["count"] for e in enrollment_growth}

        enrollment_growth_labels = [
            str((last_week + timedelta(days=i))) for i in range(7)
        ]
        enrollment_growth_data = [
            enrollment_growth_dict.get(day, 0) for day in enrollment_growth_labels
        ]

        extra_context = extra_context or {}
        extra_context.update(
            {
                "users_count": users_count,
                "courses_count": courses_count,
                "enrollments_count": enrollments_count,
                "blogs_count": blogs_count,
                "deletions_count": deletions_count,
                "user_growth_labels": user_growth_labels,
                "user_growth_data": user_growth_data,
                "enrollment_growth_labels": enrollment_growth_labels,
                "enrollment_growth_data": enrollment_growth_data,
            }
        )
        return super().index(request, extra_context=extra_context)


# Register admin site
custom_admin_site = CustomAdminSite(name="custom_admin")

# Register models with custom site
custom_admin_site.register(User)
custom_admin_site.register(Profile)
custom_admin_site.register(Course)
custom_admin_site.register(Lesson)
custom_admin_site.register(Enrollment)
custom_admin_site.register(Blog)
custom_admin_site.register(AccountDeletionLog)
