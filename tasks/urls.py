from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('task/', views.task, name='task'),
    path('planner/', views.planner, name='planner'),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup, name='signup'),
    path('delete/<int:id>/', views.delete_task, name='delete_task'),
    path('complete/<int:id>/', views.complete_task, name='complete_task'),
    path("logout/", views.logout_view, name="logout"),
    

]