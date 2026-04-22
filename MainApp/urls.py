from django.urls import path
from . import views

app_name = 'MainApp'

urlpatterns = [
    path('', views.skill_list, name='skill_list'),
    path('skill/<int:pk>/', views.skill_detail, name='skill_detail'),
    path('skill/create/', views.skill_create, name='skill_create'),
    path('skill/<int:pk>/edit/', views.skill_update, name='skill_update'),
    path('skill/<int:pk>/delete/', views.skill_delete, name='skill_delete'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('register/', views.register_user, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]