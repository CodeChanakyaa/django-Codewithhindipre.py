from django.db import models
from ckeditor.fields import RichTextField
from autoslug import AutoSlugField
from django.contrib.auth.models import User

SUBSCRIPTIONS = (
    ('Free', 'Free'),
    ('Premium', 'Premium'),
)

class ProfileModel(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    profile_id = models.IntegerField(default=None, null=True, blank=True)
    profile_image = models.ImageField(upload_to="profileimage", blank=True, null=True)
    is_pro = models.BooleanField(default=False)
    subscription_type = models.CharField(max_length=100, choices=SUBSCRIPTIONS, default="Free")

    def __str__(self):
        return self.user.first_name

class CourseModel(models.Model):
    course_name = models.CharField(max_length=100)
    course_image = models.ImageField(upload_to='courseimage')
    course_desc = RichTextField()
    is_premium = models.BooleanField(default=False)
    slug = AutoSlugField(populate_from='course_name', unique=True)

    def __str__(self):
        return self.course_name


class CourseModulesModel(models.Model):
    course = models.ForeignKey(CourseModel, on_delete=models.CASCADE, blank=True, related_name='coursemodules')
    course_module_name = models.CharField(max_length=250)
    course_module_desc = RichTextField()
    video_url = models.URLField(max_length=250, null=True, blank=True)
    can_view = models.BooleanField(default=False)
    course_module_slug = AutoSlugField(populate_from='course_module_name', unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author_name = models.CharField(max_length=100, null=True, blank=True, default="CodeWithNc")

    def __str__(self):
        return self.course_module_name


class BlogModel(models.Model):
    blog_name = models.CharField(max_length=100)
    blog_image = models.ImageField(upload_to='blogimage')
    blog_desc = RichTextField()
    slug = AutoSlugField(populate_from='blog_name', unique=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    blog_author = models.CharField(max_length=100, null=True, blank=True, default="CodeWithNc")

    def __str__(self):
        return self.blog_name


class ContactModel(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=100)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
