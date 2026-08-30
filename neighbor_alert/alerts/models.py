import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models


# ১. Custom User Model
class User(AbstractUser):
  ROLE_CHOICES = (
      ('admin', 'Admin'),
      ('resident', 'Resident'),
      ('moderator', 'Moderator'),
  )

  id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
  phone = models.CharField(max_length=15, blank=True, null=True)
  location = models.CharField(max_length=255, blank=True, null=True)
  latitude = models.FloatField(blank=True, null=True)
  longitude = models.FloatField(blank=True, null=True)
  role = models.CharField(
      max_length=15, choices=ROLE_CHOICES, default='resident'
  )
  created_at = models.DateTimeField(auto_now_add=True)


# ২. Emergency Alert Model
class Emergency(models.Model):
  TYPE_CHOICES = (
      ('Fire', 'Fire 🔥'),
      ('Flood', 'Flood 🌧️'),
      ('Accident', 'Road Accident 🚗'),
      ('Crime', 'Crime / Security 🚨'),
      ('Medical', 'Medical Emergency 🚑'),
      ('Other', 'Other Emergency ⚠️'),
  )

  SEVERITY_CHOICES = (
      ('High', 'High 🔴'),
      ('Medium', 'Medium 🟠'),
      ('Low', 'Low 🟡'),
  )

  STATUS_CHOICES = (
      ('Pending', 'Pending ⏳'),
      ('Verified', 'Verified 🟢'),
      ('Resolved', 'Resolved ✅'),
      ('Rejected', 'Rejected ❌'),
  )

  id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
  user = models.ForeignKey(
      User,
      on_delete=models.CASCADE,
      related_name='emergencies',
      null=True,
      blank=True,
  )
  type = models.CharField(max_length=20, choices=TYPE_CHOICES)
  title = models.CharField(max_length=200)
  description = models.TextField()
  location = models.CharField(max_length=255)
  latitude = models.FloatField(blank=True, null=True)
  longitude = models.FloatField(blank=True, null=True)
  severity = models.CharField(
      max_length=10, choices=SEVERITY_CHOICES, default='High'
  )
  image = models.ImageField(
      upload_to='emergency_images/', blank=True, null=True
  )
  status = models.CharField(
      max_length=15, choices=STATUS_CHOICES, default='Pending'
  )
  is_iot_triggered = models.BooleanField(default=False)
  created_at = models.DateTimeField(auto_now_add=True)

  class Meta:
    ordering = ['-created_at']


# ৩. Community Post Model
class Post(models.Model):
  CATEGORY_CHOICES = (
      ('Help', '🆘 Help Needed'),
      ('LostFound', '🔎 Lost & Found'),
      ('Announcement', '📣 Local Announcement'),
      ('Event', '🎉 Community Event'),
      ('Issue', '🏠 Neighborhood Issue'),
      ('General', '💡 General Discussion'),
  )

  id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
  user = models.ForeignKey(
      User, on_delete=models.CASCADE, related_name='community_posts'
  )
  category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
  title = models.CharField(max_length=200)
  content = models.TextField()
  location = models.CharField(max_length=255, blank=True, null=True)
  status = models.CharField(max_length=15, default='Active')
  created_at = models.DateTimeField(auto_now_add=True)

  class Meta:
    ordering = ['-created_at']


# ৪. Comment Model
class Comment(models.Model):
  id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
  post = models.ForeignKey(
      Post, on_delete=models.CASCADE, related_name='comments'
  )
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  text = models.TextField()
  created_at = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return f"{self.user.username} - {self.text[:30]}"