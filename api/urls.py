from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from . import api_views

router = DefaultRouter()
router.register(r'services', api_views.ServiceViewSet, basename='service')
router.register(r'projects', api_views.ProjectViewSet, basename='project')
router.register(r'updates', api_views.UpdateViewSet, basename='update')
router.register(r'clients', api_views.ClientViewSet, basename='client')
router.register(r'statistics', api_views.StatisticViewSet, basename='statistic')
router.register(r'jobs', api_views.JobViewSet, basename='job')
router.register(r'job-applications', api_views.JobApplicationViewSet, basename='job-application')
router.register(r'contact', api_views.ContactInquiryViewSet, basename='contact')
router.register(r'quotes', api_views.QuoteRequestViewSet, basename='quote')
router.register(r'appointments', api_views.AppointmentViewSet, basename='appointment')
router.register(r'work-with-us', api_views.WorkWithUsInquiryViewSet, basename='work-with-us')
router.register(r'company-profile', api_views.CompanyProfileViewSet, basename='company-profile')

urlpatterns = [
    path('', include(router.urls)),
    path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
