import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Prompt, Tag
import redis
from django.conf import settings

# Initialize Redis connection
r = redis.from_url(settings.REDIS_URL, decode_responses=True)

def prompt_list(request):
    """List all prompts or handle tagging filter."""
    if request.method == "GET":
        tag_name = request.GET.get('tag')
        if tag_name:
            prompts = Prompt.objects.filter(tags__name=tag_name)
        else:
            prompts = Prompt.objects.all()
        
        data = []
        for p in prompts:
            data.append({
                "id": p.id,
                "title": p.title,
                "complexity": p.complexity,
                "created_at": p.created_at.isoformat(),
                "tags": [t.name for t in p.tags.all()]
            })
        return JsonResponse(data, safe=False)

@csrf_exempt
def login_user(request):
    if request.method == "POST":
        try:
            body = json.loads(request.body)
            username = body.get('username')
            password = body.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return JsonResponse({"message": "Login successful", "user": username})
            return JsonResponse({"error": "Invalid credentials"}, status=401)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
    return JsonResponse({"error": "Method not allowed"}, status=405)

@csrf_exempt
def logout_user(request):
    logout(request)
    return JsonResponse({"message": "Logout successful"})

@csrf_exempt
def create_prompt(request):
    """Create a new prompt (Requires Authentication)."""
    if not request.user.is_authenticated:
        return JsonResponse({"error": "Authentication required"}, status=401)

    if request.method == "POST":
        try:
            body = json.loads(request.body)
            title = body.get('title')
            content = body.get('content')
            complexity = body.get('complexity', 1)
            tags_data = body.get('tags', [])

            # Validation
            if not title or len(title) < 3:
                return JsonResponse({"error": "Title must be at least 3 characters"}, status=400)
            if not content or len(content) < 20:
                return JsonResponse({"error": "Content must be at least 20 characters"}, status=400)
            try:
                complexity = int(complexity)
                if not (1 <= complexity <= 10):
                    raise ValueError
            except (ValueError, TypeError):
                return JsonResponse({"error": "Complexity must be between 1 and 10"}, status=400)

            prompt = Prompt.objects.create(
                title=title,
                content=content,
                complexity=complexity
            )

            # Handle Tags
            for tag_name in tags_data:
                tag, _ = Tag.objects.get_or_create(name=tag_name.strip().lower())
                prompt.tags.add(tag)

            return JsonResponse({
                "id": prompt.id,
                "title": prompt.title,
                "complexity": prompt.complexity,
                "message": "Prompt created successfully"
            }, status=201)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
    
    return JsonResponse({"error": "Method not allowed"}, status=405)

def prompt_detail(request, pk):
    """Retrieve a single prompt and increment view count."""
    if request.method == "GET":
        prompt = get_object_or_404(Prompt, pk=pk)
        
        # Redis View Counter
        redis_key = f"prompt:{prompt.id}:views"
        view_count = r.get(redis_key) or 0
        r.incr(redis_key)
        # Note: incr returns the new value, but let's be safe
        view_count = int(view_count) + 1
        
        data = {
            "id": prompt.id,
            "title": prompt.title,
            "content": prompt.content,
            "complexity": prompt.complexity,
            "created_at": prompt.created_at.isoformat(),
            "view_count": view_count,
            "tags": [t.name for t in prompt.tags.all()]
        }
        return JsonResponse(data)
    
    return JsonResponse({"error": "Method not allowed"}, status=405)