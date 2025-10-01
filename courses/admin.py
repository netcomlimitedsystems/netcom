from django.contrib import admin
from .models import Course, Lesson, Enrollment, Blog


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "level", "author", "created_at", "updated_at")
    search_fields = ("title", "description")
    list_filter = ("category", "level", "created_at")
    date_hierarchy = "created_at"


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ("title", "course", "duration", "created_at")
    search_fields = ("title", "content")
    list_filter = ("course", "created_at")


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ("user", "course", "enrolled_at")
    search_fields = ("user__username", "course__title")
    list_filter = ("enrolled_at",)
    date_hierarchy = "enrolled_at"


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "author", "published_at", "updated_at")
    search_fields = ("title", "content")
    list_filter = ("category", "published_at")
    date_hierarchy = "published_at"
