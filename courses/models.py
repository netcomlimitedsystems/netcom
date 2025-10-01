
from django.db import models
from django.contrib.auth.models import User


class Course(models.Model):
    LEVEL_CHOICES = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    ]
    CATEGORY_CHOICES = [
        ('cybersecurity', 'Cybersecurity'),
        ('software', 'Software Development'),
        ('cloud', 'Cloud Computing'),
        ('devops', 'DevOps'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES, default='beginner')
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="courses")
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default="software")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="lessons")
    title = models.CharField(max_length=200)
    content = models.TextField()
    video_url = models.URLField(blank=True, null=True)
    duration = models.DurationField(blank=True, null=True, help_text="Duration of the lesson (HH:MM:SS)")
    created_at = models.DateTimeField(auto_now_add=True)
    uploaded_at = models.DateTimeField(auto_now=True)  # auto updates on save

    def __str__(self):
        return f"{self.course.title} - {self.title}"


class Enrollment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="enrollments")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="enrollments")
    enrolled_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'course')  # prevent duplicate enrollments

    def __str__(self):
        return f"{self.user.username} enrolled in {self.course.title}"


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="course_profile")
    bio = models.TextField(blank=True, null=True)
    profile_image = models.ImageField(upload_to="profiles/", default="profiles/default.png")
    website = models.URLField(blank=True, null=True)
    github = models.URLField(blank=True, null=True)
    linkedin = models.URLField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"


class Blog(models.Model):
    CATEGORY_CHOICES = [
        ('cybersecurity', 'Cybersecurity'),
        ('software_dev', 'Software Development'),
        ('general', 'General'),
    ]

    title = models.CharField(max_length=200)
    content = models.TextField()
    image = models.ImageField(upload_to="blogs/", blank=True, null=True)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default="general")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="blogs")
    published_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-published_at"]

    def __str__(self):
        return self.title
