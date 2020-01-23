from rest_framework import viewsets
from rest_framework import mixins
from .models import UserFav
from .serializers import UserFavSerializer,UserFavDetailSerializer
from rest_framework.permissions import IsAuthenticated
from utils.permissions import IsOwnerOrReadOnly
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.authentication import SessionAuthentication
#mixins.CreateModelMixin        添加收藏（相当于创建数据库）
#mixins.DestroyModelMixin      取消删除（相当于数据库删除）
#mixins.ListModelMixin             获取已收藏的商品列表
class UserFavViewset(mixins.CreateModelMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin,mixins.DestroyModelMixin, viewsets.GenericViewSet):
    """
    list:
        获取用户收藏列表
    retrieve:
        判断某个商品是否已经收藏
    create:
        收藏商品
    """
    #serializer_class = UserFavSerializer
    #动态选择serializer
    def get_serializer_class(self):
        if self.action == "list":
            return UserFavDetailSerializer
        elif self.action == 'create':
            return UserFavSerializer
        return UserFavSerializer
    #permission是用来做判断权限的
    #IsAuthenticated :必须登录用户 IsOwerORReadOnly 必须是当前登录的用户
    #只有登录用户才可以收藏
    #用户只能获取自己的收藏，不能获取所有用户的收藏
    permission_classes = (IsAuthenticated,IsOwnerOrReadOnly)
    #auth使用来做用户验证的
    #JSONWebTokenAuthentication认证不应该全局配置，因为用户获取商品信息或者其它页面的时候并不需要此认证，所以这个认证只要局部中添加就可以
    #删除settings中的'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
    authentication_classes = (JSONWebTokenAuthentication,SessionAuthentication)
    #搜索字段
    lookup_field = 'goods_id'

    def get_queryset(self):
        #只能查看当前登录用户的收藏 不会获取所有用户的收藏
        #return UserFav.objects.filter(user=self.request.user)
        return UserFav.objects.filter(user=self.request.user)

