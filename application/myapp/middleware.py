import json

from django.http import JsonResponse

from rate_limiter.rate_limiter import RateLimiter
from .utils import fetch_redis_client


class RateLimitedMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response
        self.rate_limiter = RateLimiter('fixed_window', fetch_redis_client())

    def __call__(self, request):
        identifiers = [request.path[1:], "ip", request.META.get('REMOTE_ADDR')]
        # print(request.META)
        # print(identifiers)
        if self.rate_limiter.is_rate_limited(identifiers):
            return JsonResponse({
                'error': 'Too many requests, please try again later.'
            }, status=429)

        response = self.get_response(request)
        return response
