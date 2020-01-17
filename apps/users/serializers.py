import re
from datetime import datetime,timedelta
from shop3.settings import REGEX_MOBILE
from users.models import VerifyCode
from rest_framework import serializers
from django.contrib.auth import get_user_model
User = get_user_model()

class SmsSerializer(serializers.Serializer):
    mobile = serializers.CharField(max_length=11)
    def validate_mobile(self,mobile):
        ''''手机号验证'''
        #是否已经注册
        if  User.objects.filter(mobile=mobile).count():
            raise serializers.ValidationError('用户已经存在')
        #是否合法
        if not re.match(REGEX_MOBILE,mobile):
            raise serializers.ValidationError('手机号码非法')
        one_mintes_ago = datetime.now() - timedelta(hours=0,minutes=1,seconds=0)
        if VerifyCode.objects.filter(add_time__gt=one_mintes_ago,mobile=mobile).count()
            raise serializers.ValidationError("距离上一次发送未超过60s")
        return mobile