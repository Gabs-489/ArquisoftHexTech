from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.db import connection

def index(request):
    return HttpResponse(status=204)

def health_check(request):
    try:
        # Intentamos hacer un query simple
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")

        return JsonResponse({'status': 'ok'}, status=200)
    except Exception as e:
        return JsonResponse({'status': 'unhealthy', 'error': str(e)}, status=503)