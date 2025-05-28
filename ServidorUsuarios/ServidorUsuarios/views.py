from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.db import connection
from pymongo import MongoClient

from ServidorUsuarios.settings import MONGO_CLI

def index(request):
    return HttpResponse(status=204)

def health_check(request):
    try:
        client = MongoClient(MONGO_CLI, serverSelectionTimeoutMS=1000)
        client.admin.command('ping')  

        return JsonResponse({'status': 'ok'}, status=200)
    except Exception as e:
        return JsonResponse({'status': 'unhealthy', 'error': str(e)}, status=503)