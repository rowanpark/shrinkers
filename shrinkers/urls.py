"""
URL configuration for shrinkers project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.conf.urls import url
from django.contrib import admin
from django.urls import include, path  # include: django 2.0 이후 버전에서 사용되는 것
# from django.conf.urls import include  # django 2.0 이전 버전과의 하위 호환성을 제공
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from ninja import NinjaAPI
from rest_framework import permissions

from shortener.urls.views import url_redirect
from shortener.urls.urls import router as url_router
from shortener.users.apis import user as user_router
from shrinkers.settings import DEBUG
# if DEBUG:
#     import debug_toolbar


schema_view = get_schema_view(
    openapi.Info(
        title='Shrinkers API',
        default_version='v1',
        description='test description',
        terms_of_service='https://www.google.com/policies/terms/',
        contact=openapi.Contact(email='contact@snippets.local'),
        license=openapi.License(name='BSD License'),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

apis = NinjaAPI(title='Shrinkers API')
apis.add_router('/users/', user_router, tags=['Common'])  # tags: 아무거나

urlpatterns = [
    url(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    url(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    url(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('admin/', admin.site.urls),
    path('', include('shortener.index.urls')),
    path('urls/', include('shortener.urls.urls')),
    path('api/', include(url_router.urls)),
    path('ninja-api/', apis.urls),
    path('<str:prefix>/<str:url>', url_redirect),
]

# if DEBUG:
#     urlpatterns += [
#         path('__debug__/', include(debug_toolbar.urls)),  # Django Debug Toolbar
#     ]
