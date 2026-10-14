from datetime import date

from django.contrib import admin, messages
from django.contrib.auth import get_user_model

from .models import ContactInquiry, QuoteRequest, WorkWithUsInquiry, Appointment


class ReadOnlySubmissionMixin:
    """Submissions come from the public site - staff manage status but can't fabricate entries."""

    def has_add_permission(self, request):
        return False


class FollowUpFilter(admin.SimpleListFilter):
    title = 'follow-up'
    parameter_name = 'follow_up'

    def lookups(self, request, model_admin):
        return [('overdue', 'Overdue'), ('today', 'Due today'), ('upcoming', 'Upcoming'), ('none', 'Not set')]

    def queryset(self, request, queryset):
        today = date.today()
        open_states = ['new', 'in_progress', 'quoted']
        value = self.value()
        if value == 'overdue':
            return queryset.filter(follow_up_date__lt=today, status__in=open_states)
        if value == 'today':
            return queryset.filter(follow_up_date=today, status__in=open_states)
        if value == 'upcoming':
            return queryset.filter(follow_up_date__gt=today)
        if value == 'none':
            return queryset.filter(follow_up_date__isnull=True)
        return queryset


class LeadAdminMixin(ReadOnlySubmissionMixin):
    """Shared lead-tracker behaviour: quick status actions, assignee limited to staff."""
    actions = ['mark_in_progress', 'mark_quoted', 'mark_won', 'mark_lost']

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'assigned_to':
            kwargs['queryset'] = get_user_model().objects.filter(is_staff=True, is_active=True)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def _bulk_status(self, request, queryset, status, label):
        count = queryset.update(status=status)
        self.message_user(request, f'{count} lead(s) marked as {label}.', messages.SUCCESS)

    @admin.action(description='Mark selected as Contacted / In Progress')
    def mark_in_progress(self, request, queryset):
        self._bulk_status(request, queryset, 'in_progress', 'Contacted / In Progress')

    @admin.action(description='Mark selected as Quote Sent')
    def mark_quoted(self, request, queryset):
        self._bulk_status(request, queryset, 'quoted', 'Quote Sent')

    @admin.action(description='Mark selected as Won')
    def mark_won(self, request, queryset):
        self._bulk_status(request, queryset, 'won', 'Won')

    @admin.action(description='Mark selected as Lost')
    def mark_lost(self, request, queryset):
        self._bulk_status(request, queryset, 'lost', 'Lost')


@admin.register(ContactInquiry)
class ContactInquiryAdmin(LeadAdminMixin, admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'inquiry_type', 'subject', 'status',
                    'assigned_to', 'follow_up_date', 'created_at')
    list_editable = ('status', 'assigned_to', 'follow_up_date')
    list_filter = ('status', FollowUpFilter, 'inquiry_type', 'created_at')
    search_fields = ('name', 'email', 'phone', 'subject', 'message', 'internal_notes')
    readonly_fields = ('name', 'email', 'phone', 'subject', 'inquiry_type', 'message', 'created_at')
    date_hierarchy = 'created_at'


@admin.register(QuoteRequest)
class QuoteRequestAdmin(LeadAdminMixin, admin.ModelAdmin):
    list_display = ('name', 'company', 'phone', 'service', 'estimated_budget', 'status',
                   'assigned_to', 'follow_up_date', 'deal_value', 'created_at')
    list_editable = ('status', 'assigned_to', 'follow_up_date')
    list_filter = ('status', FollowUpFilter, 'service', 'estimated_budget', 'created_at')
    search_fields = ('name', 'company', 'email', 'phone', 'service', 'message', 'internal_notes')
    readonly_fields = (
        'name', 'company', 'email', 'phone', 'service', 'project_type',
        'project_location', 'estimated_budget', 'expected_start_date',
        'message', 'attachment', 'created_at',
    )
    date_hierarchy = 'created_at'


@admin.register(WorkWithUsInquiry)
class WorkWithUsInquiryAdmin(LeadAdminMixin, admin.ModelAdmin):
    list_display = ('full_name', 'company_name', 'organization_type', 'phone', 'status',
                    'assigned_to', 'follow_up_date', 'created_at')
    list_editable = ('status', 'assigned_to', 'follow_up_date')
    list_filter = ('status', FollowUpFilter, 'organization_type', 'created_at')
    search_fields = ('full_name', 'company_name', 'email', 'phone', 'message', 'internal_notes')
    readonly_fields = (
        'full_name', 'company_name', 'email', 'phone', 'organization_type',
        'project_type', 'project_location', 'message', 'created_at',
    )
    date_hierarchy = 'created_at'


@admin.register(Appointment)
class AppointmentAdmin(ReadOnlySubmissionMixin, admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'preferred_date', 'preferred_time', 'status', 'created_at')
    list_editable = ('status',)
    list_filter = ('status', 'preferred_date')
    search_fields = ('name', 'email', 'phone')
    readonly_fields = ('name', 'email', 'phone', 'preferred_date', 'preferred_time', 'message', 'created_at')
    date_hierarchy = 'preferred_date'
