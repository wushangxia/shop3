from rest_framework import serializers
from user_operation.models import UserFav
from rest_framework.validators import UniqueTogetherValidator

class UserFavSerializer(serializers.ModelSerializer):
    #获取当前登录用户
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        #validate实验唯一联合，一个商品只能收藏一次
        validators = [
            UniqueTogetherValidator(queryset=UserFav.objects.all(),fields=('user','goods'),message="已经收藏")
        ]
        model = UserFav
        #收藏的时候需要返回商品id，因为取消收藏的时候需要知道商品id是多少
        fields = ('user',"goods",'id')
