
import json, redis
from django.http import JsonResponse
from .models import Prompt

r = redis.Redis(host='redis', port=6379, db=0)

def prompt_list(request):
    if request.method == "GET":
        return JsonResponse(list(Prompt.objects.all().values()), safe=False)

def create_prompt(request):
    if request.method == "POST":
        data = json.loads(request.body)
        p = Prompt.objects.create(**data)
        return JsonResponse({"id": p.id})

def prompt_detail(request, id):
    p = Prompt.objects.get(id=id)
    views = r.incr(f"prompt:{id}:views")
    return JsonResponse({
        "id": p.id,
        "title": p.title,
        "content": p.content,
        "complexity": p.complexity,
        "view_count": views
    })
