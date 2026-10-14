from .models import CompanyProfile


class CompanyProfileMiddleware:
    """
    Ensures a CompanyProfile row always exists, seeded with the values
    supplied by Highnoon Engineering Solutions, so the site never renders
    with empty contact information on first run.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path != '/health/' and not CompanyProfile.objects.exists():
            CompanyProfile.objects.create()
        return self.get_response(request)
