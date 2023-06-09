"""service_backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/', include('service_backend.apps.users.urls')),
    path('issue/', include('service_backend.apps.issues.urls')),
    path('subject/', include('service_backend.apps.subjects.urls')),
    path('chapter/', include('service_backend.apps.chapters.urls')),
    path('tag/', include('service_backend.apps.tags.urls')),
    path('year/', include('service_backend.apps.years.urls')),
    path('admins/', include('service_backend.apps.admins.urls')),
    path('images/', include('service_backend.apps.images.urls')),
    path('mail/', include('service_backend.apps.mail.urls')),
    path('notification/', include('service_backend.apps.notifications.urls'))
]
