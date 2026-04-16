
from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse

def home(request):
    return HttpResponse("AI Prompt Library Running 🚀")

urlpatterns = [
    path('', home),
    path('admin/', admin.site.urls),
    path('prompts/', include('prompts.urls')),
]