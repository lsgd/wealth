import logging
import uuid

logger = logging.getLogger(__name__)


class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.request_id = str(uuid.uuid4())[:8]

        # Log request
        logger.info('request_started', extra={
            'request_id': request.request_id,
            'method': request.method,
            'path': request.path,
            'user': str(request.user) if hasattr(request, 'user') else 'anonymous',
        })

        response = self.get_response(request)

        # Log response
        logger.info('request_finished', extra={
            'request_id': request.request_id,
            'status_code': response.status_code,
        })

        return response
