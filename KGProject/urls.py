"""KGProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path,include
from django.conf.urls import url
#利用TemplateView
from django.views.generic import TemplateView
#导入neo模的接口
from neo import views

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('', include('home.urls')),
    url(r'^$', TemplateView.as_view(template_name="index.html")),
    url(r'^matchAll', views.match_all),
    url(r'^searchByTitle', views.search_by_title),
    url(r'^searchByKeyword', views.search_by_keyword),
    url(r'^searchByAuthor', views.search_by_author),
    url(r'^searchTitleByAlgorithm', views.search_title_by_algorithm),
    url(r'^search', views.search_entity),
]
