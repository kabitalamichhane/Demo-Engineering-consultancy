from rest_framework import serializers

from company.models import CompanyProfile, Statistic, Client
from services.models import Service
from projects.models import Project, ProjectImage
from updates.models import Update
from careers.models import Job, JobApplication
from inquiries.models import ContactInquiry, QuoteRequest, WorkWithUsInquiry, Appointment
from company.security import (
    validate_uploaded_file, ALLOWED_DOCUMENT_EXTENSIONS, ALLOWED_IMAGE_EXTENSIONS,
)


class CompanyProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyProfile
        fields = [
            'company_name', 'short_name', 'tagline', 'description',
            'hero_heading', 'hero_subtext', 'hero_image',
            'hero_button_1_text', 'hero_button_1_url',
            'hero_button_2_text', 'hero_button_2_url',
            'hero_button_3_text', 'hero_button_3_url',
            'director_name', 'director_designation', 'director_photo', 'director_quote',
            'showcase_image', 'showcase_title', 'showcase_text', 'showcase_caption',
            'team_photo', 'team_heading', 'team_text',
            'address_line', 'city', 'country', 'postal_code',
            'phone', 'email', 'map_embed_url',
            'facebook_url', 'linkedin_url', 'instagram_url', 'youtube_url',
            'logo', 'favicon',
            'default_seo_title', 'default_seo_description', 'updated_at',
        ]
        read_only_fields = fields


class StatisticSerializer(serializers.ModelSerializer):
    class Meta:
        model = Statistic
        fields = ['id', 'title', 'value', 'icon', 'display_order', 'active']


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ['id', 'name', 'logo', 'website', 'description', 'active', 'display_order']


class ServiceSerializer(serializers.ModelSerializer):
    feature_list = serializers.ReadOnlyField()

    class Meta:
        model = Service
        fields = [
            'id', 'name', 'slug', 'short_description', 'description', 'features',
            'feature_list', 'image', 'icon', 'seo_title', 'seo_description',
            'display_order', 'active', 'created_at', 'updated_at',
        ]


class ProjectImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectImage
        fields = ['id', 'image', 'caption', 'display_order']


class ProjectSerializer(serializers.ModelSerializer):
    gallery_images = ProjectImageSerializer(many=True, read_only=True)
    category_display = serializers.CharField(source='get_category_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = Project
        fields = [
            'id', 'name', 'slug', 'client', 'location', 'category', 'category_display',
            'status', 'status_display', 'start_date', 'completion_date', 'description',
            'scope', 'project_value', 'featured_image', 'gallery_images', 'featured',
            'is_demo', 'seo_title', 'seo_description', 'created_at', 'updated_at',
        ]


class ProjectListSerializer(serializers.ModelSerializer):
    """Lighter serializer for list views."""
    category_display = serializers.CharField(source='get_category_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = Project
        fields = [
            'id', 'name', 'slug', 'client', 'location', 'category', 'category_display',
            'status', 'status_display', 'completion_date', 'featured_image', 'featured', 'is_demo',
        ]


class UpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Update
        fields = [
            'id', 'title', 'slug', 'featured_image', 'excerpt', 'content', 'category',
            'author', 'published', 'published_at', 'seo_title', 'seo_description',
            'created_at', 'updated_at',
        ]


class JobSerializer(serializers.ModelSerializer):
    responsibility_list = serializers.ReadOnlyField()
    requirement_list = serializers.ReadOnlyField()

    class Meta:
        model = Job
        fields = [
            'id', 'title', 'slug', 'department', 'location', 'employment_type',
            'description', 'responsibilities', 'responsibility_list',
            'requirements', 'requirement_list', 'deadline', 'active', 'created_at',
        ]


class JobApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobApplication
        fields = ['id', 'job', 'full_name', 'email', 'phone', 'cover_letter', 'resume', 'created_at']
        read_only_fields = ['created_at']

    def validate_job(self, job):
        if not job.active:
            raise serializers.ValidationError('This position is no longer accepting applications.')
        return job

    def validate_resume(self, value):
        return validate_uploaded_file(value, allowed_extensions=ALLOWED_DOCUMENT_EXTENSIONS)


class ContactInquirySerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactInquiry
        fields = ['id', 'name', 'email', 'phone', 'subject', 'inquiry_type', 'message', 'status', 'created_at']
        read_only_fields = ['status', 'created_at']


class QuoteRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuoteRequest
        fields = [
            'id', 'name', 'company', 'email', 'phone', 'service', 'project_type',
            'project_location', 'estimated_budget', 'expected_start_date', 'message',
            'attachment', 'status', 'created_at',
        ]
        read_only_fields = ['status', 'created_at']

    def validate_attachment(self, value):
        return validate_uploaded_file(
            value,
            allowed_extensions=ALLOWED_DOCUMENT_EXTENSIONS + ALLOWED_IMAGE_EXTENSIONS,
        )


class WorkWithUsInquirySerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkWithUsInquiry
        fields = [
            'id', 'full_name', 'company_name', 'email', 'phone', 'organization_type',
            'project_type', 'project_location', 'message', 'status', 'created_at',
        ]
        read_only_fields = ['status', 'created_at']


class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = [
            'id', 'name', 'email', 'phone', 'preferred_date', 'preferred_time',
            'message', 'status', 'created_at',
        ]
        read_only_fields = ['status', 'created_at']
