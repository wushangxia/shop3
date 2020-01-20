from rest_framework import viewsets
from rest_framework import mixins
from .models import UserFav
from .serializers import UserFavSerializer
#mixins.CreateModelMixin        添加收藏（相当于创建数据库）
#mixins.DestroyModelMixin      取消删除（相当于数据库删除）
#mixins.ListModelMixin             获取已收藏的商品列表
class UserFavViewset(mixins.CreateModelMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin,mixins.DestroyModelMixin, viewsets.GenericViewSet):
    "用户收藏"
    queryset = UserFav.objects.all()
    serializer_class = UserFavSerializer
