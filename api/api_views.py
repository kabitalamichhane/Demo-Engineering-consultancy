from rest_framework import viewsets, mixins, generics
from rest_framework.permissions import AllowAny

from company.models import CompanyProfile, Statistic, Client
from services.models import Service
from projects.models import Project
from updates.models import Update
from careers.models import Job, JobApplication
from inquiries.models import ContactInquiry, QuoteRequest, WorkWithUsInquiry, Appointment

from .serializers import (
    CompanyProfileSerializer, StatisticSerializer, ClientSerializer,
    ServiceSerializer, ProjectSerializer, ProjectListSerializer, UpdateSerializer,
    JobSerializer, JobApplicationSerializer, ContactInquirySerializer,
    QuoteRequestSerializer, WorkWithUsInquirySerializer, AppointmentSerializer,
)
from .permissions import IsAdminOrReadOnly, IsAdminOnly
from .throttles import FormSubmitThrottleMixin


# ---------------------------------------------------------------------------
# Public, read-mostly resources (writes restricted to staff)
# ---------------------------------------------------------------------------
class CompanyProfileViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """Read-only: exposes the single CompanyProfile row."""
    queryset = CompanyProfile.objects.all()
    serializer_class = CompanyProfileSerializer
    permission_classes = [AllowAny]

    def list(self, request, *args, **kwargs):
        from rest_framework.response import Response
        profile = CompanyProfile.objects.first()
        serializer = self.get_serializer(profile)
        return Response(serializer.data)


class ServiceViewSet(viewsets.ModelViewSet):
    serializer_class = ServiceSerializer
    permission_classes = [IsAdminOrReadOnly]
    lookup_field = 'slug'
    filterset_fields = ['active']
    search_fields = ['name', 'short_description', 'description']
    ordering_fields = ['display_order', 'name', 'created_at']

    def get_queryset(self):
        qs = Service.objects.all()
        if not (self.request.user and self.request.user.is_staff):
            qs = qs.filter(active=True)
        return qs


class ProjectViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminOrReadOnly]
    lookup_field = 'slug'
    filterset_fields = ['category', 'status', 'featured', 'is_demo']
    search_fields = ['name', 'client', 'location', 'description']
    ordering_fields = ['completion_date', 'created_at', 'name']

    def get_queryset(self):
        return Project.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return ProjectListSerializer
        return ProjectSerializer


class UpdateViewSet(viewsets.ModelViewSet):
    serializer_class = UpdateSerializer
    permission_classes = [IsAdminOrReadOnly]
    lookup_field = 'slug'
    filterset_fields = ['category', 'published']
    search_fields = ['title', 'excerpt', 'content']
    ordering_fields = ['published_at', 'created_at']

    def get_queryset(self):
        qs = Update.objects.all()
        if not (self.request.user and self.request.user.is_staff):
            qs = qs.filter(published=True)
        return qs


class ClientViewSet(viewsets.ModelViewSet):
    serializer_class = ClientSerializer
    permission_classes = [IsAdminOrReadOnly]
    filterset_fields = ['active']

    def get_queryset(self):
        qs = Client.objects.all()
        if not (self.request.user and self.request.user.is_staff):
            qs = qs.filter(active=True)
        return qs


class StatisticViewSet(viewsets.ModelViewSet):
    serializer_class = StatisticSerializer
    permission_classes = [IsAdminOrReadOnly]
    filterset_fields = ['active']

    def get_queryset(self):
        qs = Statistic.objects.all()
        if not (self.request.user and self.request.user.is_staff):
            qs = qs.filter(active=True)
        return qs


class JobViewSet(viewsets.ModelViewSet):
    serializer_class = JobSerializer
    permission_classes = [IsAdminOrReadOnly]
    lookup_field = 'slug'
    filterset_fields = ['active', 'department', 'employment_type']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'deadline']

    def get_queryset(self):
        qs = Job.objects.all()
        if not (self.request.user and self.request.user.is_staff):
            qs = qs.filter(active=True)
        return qs


# ---------------------------------------------------------------------------
# Private submission resources — public POST (create) only, staff-only read
# ---------------------------------------------------------------------------
class ContactInquiryViewSet(FormSubmitThrottleMixin, viewsets.ModelViewSet):
    queryset = ContactInquiry.objects.all()
    serializer_class = ContactInquirySerializer
    permission_classes = [IsAdminOnly]
    http_method_names = ['get', 'post', 'patch', 'delete', 'head', 'options']


class QuoteRequestViewSet(FormSubmitThrottleMixin, viewsets.ModelViewSet):
    queryset = QuoteRequest.objects.all()
    serializer_class = QuoteRequestSerializer
    permission_classes = [IsAdminOnly]
    http_method_names = ['get', 'post', 'patch', 'delete', 'head', 'options']


class WorkWithUsInquiryViewSet(FormSubmitThrottleMixin, viewsets.ModelViewSet):
    queryset = WorkWithUsInquiry.objects.all()
    serializer_class = WorkWithUsInquirySerializer
    permission_classes = [IsAdminOnly]
    http_method_names = ['get', 'post', 'patch', 'delete', 'head', 'options']


class AppointmentViewSet(FormSubmitThrottleMixin, viewsets.ModelViewSet):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    permission_classes = [IsAdminOnly]
    http_method_names = ['get', 'post', 'patch', 'delete', 'head', 'options']


class JobApplicationViewSet(FormSubmitThrottleMixin, viewsets.ModelViewSet):
    queryset = JobApplication.objects.all()
    serializer_class = JobApplicationSerializer
    permission_classes = [IsAdminOnly]
    http_method_names = ['get', 'post', 'patch', 'delete', 'head', 'options']
