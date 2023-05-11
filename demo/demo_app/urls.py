from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.registerpage, name='register'),
    path('login/', views.loginpage, name='login'),
    path('logout/', views.logoutpage, name='logout'),
    path('about/', views.about, name='about'),
    path('services/', views.services, name='services'),
    path('projects/', views.projects, name='projects'),
    path('gallery/', views.gallery, name='gallery'),
    path('contact/', views.contact, name='contact'),
    path('gas_project/', views.gas_project, name='gas_project'),
    path('energy_project/', views.energy_project, name='energy_project'),
    path('service_1/', views.service_1, name='service_1'),
    path('service_2/', views.service_2, name='service_2'),
    path('service_3/', views.service_3, name='service_3'),

    path('password_change/', views.password_change, name="password_change"),
    path('password_reset/', views.password_reset_request, name="password_reset"),
    path('reset/<uidb64>/<token>', views.passwordResetConfirm, name="password_reset_confirm"),
]