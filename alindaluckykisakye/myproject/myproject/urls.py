from django.contrib import admin
from django.urls import path
from myapp.views import login_view, dashboard_view, signup_view, success_view

urlpatterns = [
    # Root URL (Home) - points to login
    path('', login_view, name='login'),

    # Admin panel
    path('admin/', admin.site.urls),

    # Other URLs
    path('dashboard/', dashboard_view, name='dashboard'),
    path('signup/', signup_view, name='signup'),
    path('success/', success_view, name='success'),
]
