"""app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from rest_framework import permissions
from django.contrib import admin
from django.urls import path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
  openapi.Info(title="A simple blog post API Documentation",
  default_version='v1',
  description="This is the documentation of all the POST API end points.",
  terms_of_service="https://www.google.com/policies/terms/",
  contact=openapi.Contact(email="contact@snippets.local"),
  license=openapi.License(name="BSD License"),)
,public=True,
permission_classes=(permissions.AllowAny,),)


# schema_view = get_schema_view(title='Blog API')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/user/', include('user.urls')),
    path('api/post/', include('post.urls')),
    # url(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0),˓→name='schema-json'),
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-˓→swagger-ui'),
    path('doc/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-˓→swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc˓→'),
]
