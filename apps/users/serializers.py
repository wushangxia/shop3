import re
from datetime import datetime,timedelta
from shop3.settings import REGEX_MOBILE
from users.models import VerifyCode
from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.validators import UniqueValidator
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
        # 验证码发送频率
        one_mintes_ago = datetime.now() - timedelta(hours=0,minutes=1,seconds=0)
        if VerifyCode.objects.filter(add_time__gt=one_mintes_ago,mobile=mobile).count():
            raise serializers.ValidationError("距离上一次发送未超过60s")
        return mobile

class UserRegSerializer(serializers.ModelSerializer):
    """用户注册"""
    #UserProfile里面没有code的字段，这里定义一个code序列化字段
    #write_only是只写不能读，可以理解为只能前台到后台，在后台做了逻辑操作后直接存数据库，在反序列化字段使用。在下面的例子中，password就是反序列化，不需要传前台，而re_password是自定义反序列化字段，
    # 仅用作后台和密码进行比较，然后把结果返回前台，所以不存到数据库，在全局钩子使用时要pop掉
    code = serializers.CharField(required=True,write_only=True,max_length=4,min_length=4,error_messages={"blank":"请输入2验证码",
    "required":"请输入验4证码","max_length":"验证码格式不对","min_length":"验证码格式不对"},help_text="验证码")
    #验证用户名是否存在
    username = serializers.CharField(label="用户名",help_text="用户名",required=True,allow_blank=False,validators=[UniqueValidator(queryset=User.objects.all(),message="用户已经存在")])
    #输入密码的时候不显示明文
    password = serializers.CharField(style={'input_type':'password'},label=True,write_only=True)
    #验证code
    def  validate_code(self, code):
        # 最近的一个验证码
        verify_records = VerifyCode.objects.filter(mobile=self.initial_data["username"]).order_by("-add_time")
        print(37,verify_records,self.initial_data["username"],code)
        print(39,VerifyCode.objects.all())
        if verify_records:
            #最近一个验证码
            last_record = verify_records[0]
            #有效期为5分钟--测试60
            five_mintes_ago = datetime.now()- timedelta(hours=0,minutes=60,seconds=0)
            if five_mintes_ago > last_record.add_time:
                raise serializers.ValidationError("验证码过期")
            if last_record.code !=code:
                raise serializers.ValidationError('验证码错误')
        else:
            raise serializers.ValidationError('验证码错误')
    # 所有字段。attrs是字段验证合法之后返回的总的dict
    def validate(self,attrs):
        #前端那里没有mobile值到后端，这里添加
        attrs["mobile"] = attrs["username"]
        #code是自己添加的，数据库没有这个，验证完就删除掉
        del attrs["code"]
        return attrs
    #这是重载Create方法，
    def create(self, validated_data):
        #return User.objects.create(**validated_data)
        user = super(UserRegSerializer,self).create(validated_data=validated_data)
        print('serializer',validated_data['password'])
        user.set_password(validated_data['password'])
        user.save()
        return user
    class Meta:
        model = User
        fields = ("username", "code", "mobile", "password")
