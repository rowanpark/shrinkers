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

import debug_toolbar

from django.contrib import admin
from django.urls import include, path  # include: django 2.0 이후 버전에서 사용되는 것
# from django.conf.urls import include  # django 2.0 이전 버전과의 하위 호환성을 제공
# from django.urls import path

# from shortener.views import index, redirect_test
from shortener.views import index, get_user, register, login_view, logout_view, list_view, url_list

urlpatterns = [
    path('admin/', admin.site.urls),

    path('__debug__/', include(debug_toolbar.urls)),  # Django Debug Toolbar

    # path('', index, name='index_name'),
    path('', index, name='index'),
    # path('redirect', redirect_test),
    path('get_user/<int:user_id>', get_user),

    path('register', register, name='register'),
    path('login', login_view, name='login'),
    path('logout', logout_view, name='logout'),
    
    path('list', list_view, name='list_view'),
    path('list/url', url_list, name='url_list'),
]
