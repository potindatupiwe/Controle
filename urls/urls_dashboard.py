from django.urls import path

from .. import views
from django.contrib.auth.decorators import login_required
urlpatterns = [
    path('dashboard_base', login_required(views.DashboardView.as_view()), name='dashboard_base')
]