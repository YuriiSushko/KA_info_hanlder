import logging
from django.utils import timezone

logger = logging.getLogger(__name__)

class UpdateLastSeenMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if request.user.is_authenticated:
            request.user.last_seen = timezone.now()
            request.user.save(update_fields=['last_seen'])
            logger.debug(f"Updated last_seen for user {request.user} to {request.user.last_seen}")
        return response
