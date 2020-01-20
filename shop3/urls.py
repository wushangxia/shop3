"""shop3 URL Configuration

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
# from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
import xadmin
from django.views.static import serve
from shop3.settings import MEDIA_ROOT
from rest_framework.documentation import include_docs_urls
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views
from rest_framework_jwt.views import obtain_jwt_token
from goods.views import GoodsListViewSet,CategoryViewSet
from users.views import UserViewset,SmsCodeViewset
from user_operation.views import UserFavViewset
router = DefaultRouter()
router.register(r'goods', GoodsListViewSet)
router.register(r'category',CategoryViewSet)
router.register(r'codes', SmsCodeViewset)
router.register(r'users', UserViewset)
router.register(r'userfavs', UserFavViewset)
urlpatterns = [
    path('xadmin/', xadmin.site.urls),
    path('ueditor/', include('DjangoUeditor.urls')),
    path('media/<path:path>',serve,{'document_root':MEDIA_ROOT}),

    path('api-auth/',include('rest_framework.urls')),
    path('api-token-auth/', views.obtain_auth_token),
    #path('jwt-auth/', obtain_jwt_token),
    path('login/', obtain_jwt_token),
    url(r'^', include(router.urls)),

    url('docs',include_docs_urls(title='shop3')),
]
