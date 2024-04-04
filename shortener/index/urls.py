from django.urls import path

from shortener.index.views import index, login_view, logout_view, register


urlpatterns = [
    path('', index, name='index'),
    path('register', register, name='register'),
    path('login', login_view, name='login'),
    path('logout', logout_view, name='logout'),
]
