from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

def index(request):
    return HttpResponse(status=204)

def health_check(request):
    return JsonResponse({'message': 'OK'}, status=200)