"""moodsic_test URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import include, path
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

#stop favicon.ico not found warning
from django.views.generic import RedirectView
from django.conf.urls import url


urlpatterns = [
    path('', include('account.urls')),
    path('home/', include('recommend.urls')),    #Sets the default url directing to the recommend app.
    path('admin/', admin.site.urls),
    # Needed by Django, else a warning will be thrown
    url(r'^favicon\.ico$',RedirectView.as_view(url='/static/images/favicon.ico')),

]
