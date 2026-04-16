from django.urls import path
from . import views

urlpatterns = [
    path('', views.prompt_list, name='prompt-list'),
    path('create/', views.create_prompt, name='create-prompt'),
    path('<int:pk>/', views.prompt_detail, name='prompt-detail'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
]