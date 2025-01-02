"""
URL configuration for datacollation project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from data_collection import views
from django.shortcuts import redirect
from django.contrib.auth.views import LogoutView



urlpatterns = [

    # Landing page
     path('', views.member_login, name='member_login'),
     
    # Admin views
    path('admin/', admin.site.urls),
   
    # Monitor views
    path('monitor/login/', views.monitor_login, name='monitor_login'),
    path('monitor/dashboard/', views.monitor_dashboard, name='monitor_dashboard'),
    path('monitor/search-api/', views.monitor_search_api, name='monitor_search_api'),
    path('monitor/edit_member/<int:id>/', views.edit_member, name='edit_member'),
    path('monitor/delete_member/<int:id>/', views.delete_member, name='delete_member'),
    path('monitor/export_pdf/', views.export_pdf, name='export_pdf'),
    path('monitor/export_excel/', views.export_excel, name='export_excel'),
    path('monitor/logout/', views.monitor_logout, name='monitor_logout'),

    # Member views
    path('member/login/', views.member_login, name='member_login'),
    path('member/dashboard/', views.member_dashboard, name='member_dashboard'),
    path('member/generate_agent_code/', views.generate_agent_code, name='generate_agent_code'),
    path('member/logout/', views.member_logout, name='member_logout'),
]