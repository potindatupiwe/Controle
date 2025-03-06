"""
URL configuration for projeto_fic project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from controle import views
from graphene_django.views import GraphQLView
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
urlpatterns = [
    path('admin/', admin.site.urls),
    path('adm/', include('controle.urls.urls_adm')),
    path('func/',include('controle.urls.urls_func')),
    path('gerencia/',include('controle.urls.urls_gerencia')),
    path('dashboard/', include('controle.urls.urls_dashboard')),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('redirect/', views.RedirectView.as_view(), name='redirect'),
    path('pass_reset/', include('controle.urls.urls_PassReset')),
    path('graphql/', csrf_exempt(GraphQLView.as_view(graphiql=True))),
    path('logout/',views.CustomLogout.as_view(), name='logout')
]
urlpatterns+=static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)
