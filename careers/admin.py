from django.contrib import admin
from .models import Job, JobApplication


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('title', 'department', 'location', 'employment_type', 'active', 'deadline')
    list_editable = ('active',)
    list_filter = ('active', 'employment_type', 'department')
    search_fields = ('title', 'description')
    prepopulated_fields = {'slug': ('title',)}
    ordering = ('-active', '-created_at')


@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'job', 'email', 'phone', 'created_at')
    list_filter = ('job',)
    search_fields = ('full_name', 'email', 'phone')
    readonly_fields = ('job', 'full_name', 'email', 'phone', 'cover_letter', 'resume', 'created_at')
    date_hierarchy = 'created_at'

    def has_add_permission(self, request):
        return False
