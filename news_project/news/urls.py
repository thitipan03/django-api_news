from django.contrib import admin
from django.urls import include, path
from news.views import *
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.urls import path, re_path
from django.http import HttpResponseRedirect

schema_view = get_schema_view(
    openapi.Info(
        title="API Documentation",
        default_version="v1",
        description="API documentation for your project",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="your-email@example.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)
# def redirect_to_ecoborns_swagger(request):
#     return HttpResponseRedirect("https://api.ecoborns.com/api-docs/#/")
urlpatterns = [
    path('',home,name='home'),
    path('news/read/<int:id>/',new_page),
    path('api/news/',NewHtmlAPI.as_view(),name='api_home'),
    path('api/news/<int:id>/',ReadNewAPI.as_view(),name='api_home'),
    path('test/',test),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    # ReDoc UI
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    # path('swagger-external/', redirect_to_ecoborns_swagger, name='external-swagger-ui'),
]
