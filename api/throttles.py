from rest_framework.throttling import AnonRateThrottle


class FormSubmitThrottle(AnonRateThrottle):
    """Strict limit (default 5/hour per IP) on public form-submission endpoints."""
    scope = 'form_submit'


class FormSubmitThrottleMixin:
    """Adds FormSubmitThrottle to the 'create' action of a viewset."""

    def get_throttles(self):
        throttles = super().get_throttles()
        if getattr(self, 'action', None) == 'create':
            throttles.append(FormSubmitThrottle())
        return throttles
