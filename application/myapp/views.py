import json

from django.shortcuts import render

# Create your views here.

# myapp/views.py
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from rate_limiter.rate_limiter import RateLimiter
from .utils import fetch_redis_client


def limited(request):
    return HttpResponse("Welcome to my app!, Limited only")


def unlimited(request):
    return HttpResponse("Welcome to my app!, unlimited only")


@csrf_exempt
def add_rules(request):
    data = json.loads(request.body)
    identifiers = data.get('identifiers')
    time_unit = data.get('time_unit')
    rate = data.get('rate')
    # You can process the data or save it to the database here

    rate_limiter = RateLimiter('token_bucket', fetch_redis_client())
    rate_limiter.add_rules(identifiers=identifiers, time_unit=time_unit, rate=rate)

    return JsonResponse(status=200, data={"status": "rule_added"})
