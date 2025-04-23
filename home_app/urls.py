from django.urls import path
from . import views  # Import views from home_app

urlpatterns = [
    path("", views.index, name='index'),  # Homepage
    path("register/", views.register, name="register"),
    path("login/", views.login_view, name="login"),
    path("service_provider/login/", views.service_provider_login, name="service_provider_login"),
    path("service-provider/dashboard/", views.service_provider_dashboard, name="service_provider_dashboard"),
]
