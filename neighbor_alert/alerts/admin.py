from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Comment, Emergency, Post, User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
  fieldsets = UserAdmin.fieldsets + (
      (
          'Extra Info',
          {'fields': ('phone', 'location', 'latitude', 'longitude', 'role')},
      ),
  )

  add_fieldsets = UserAdmin.add_fieldsets + (
      (
          'Extra Info',
          {'fields': ('phone', 'location', 'latitude', 'longitude', 'role')},
      ),
  )

  list_display = ('username', 'email', 'phone', 'role', 'is_staff')
  list_filter = ('role', 'is_staff', 'is_superuser')


@admin.register(Emergency)
class EmergencyAdmin(admin.ModelAdmin):
  list_display = (
      'title',
      'type',
      'severity',
      'status',
      'location',
      'is_iot_triggered',
      'created_at',
  )
  list_filter = ('status', 'severity', 'type', 'is_iot_triggered')
  search_fields = ('title', 'description', 'location')
  list_editable = ('status',)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
  list_display = ('title', 'category', 'user', 'status', 'created_at')
  list_filter = ('category', 'status')
  search_fields = ('title', 'content')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
  list_display = ('user', 'post', 'text', 'created_at')
  search_fields = ('text', 'user__username', 'post__title')
  list_filter = ('created_at',)