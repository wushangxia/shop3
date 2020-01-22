from django.shortcuts import render
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q
from rest_framework.mixins import CreateModelMixin
from rest_framework import viewsets
from rest_framework.authentication import SessionAuthentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from .serializers import SmsSerializer,UserRegSerializer,UserDetailSerializer
from rest_framework.response import Response
from rest_framework import status
from utils.yunpian import YunPian
from shop3.settings import APIKEY
from random import choice
from .models import VerifyCode
from rest_framework import mixins
from rest_framework_jwt.serializers import jwt_encode_handler, jwt_payload_handler
from rest_framework import permissions
from rest_framework import authentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
User = get_user_model()

class CustomBackend(ModelBackend):
    "自定义用户验证"
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            print(12, username)
            user = User.objects.get(Q(username=username) | Q(mobile=username))
            print(13,User.objects.all())
            if user.check_password(password):
                return user
        except Exception as e:
            return None

class SmsCodeViewset(CreateModelMixin,viewsets.GenericViewSet):
    "手机验证码"
    serializer_class = SmsSerializer
    queryset = VerifyCode.objects.all()
    def generate_code(self):
        "生成四位随机验证码"
        seeds = "1234567890"
        randow_str = []
        for i in range(4):
            randow_str.append(choice(seeds))
        return "".join(randow_str)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        # 验证合法
        serializer.is_valid(raise_exception=True)
        mobile = serializer.validated_data['mobile']
        yun_pian = YunPian(APIKEY)
        #生成验证码
        code = self.generate_code()
        sms_status = yun_pian.send_sms(code=code,mobile=mobile)
        if sms_status["code"] !=0:
            return Response({
                "mobile":sms_status['msg']
            },status=status.HTTP_400_BAD_REQUEST)
        else:
            code_record =VerifyCode(code=code,mobile=mobile)
            code_record.save()
            return Response({
                "mobile": mobile
            }, status=status.HTTP_201_CREATED)
        # self.perform_create(serializer)
        # headers = self.get_success_headers(serializer.data)
        # return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class UserViewset(CreateModelMixin,mixins.RetrieveModelMixin,viewsets.GenericViewSet):
    "用户"
    #serializer_class = UserRegSerializer
    queryset = User.objects.all()
    authentication_classes = (SessionAuthentication,JSONWebTokenAuthentication)
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer)
        print(73,user)
        re_dict = serializer.data
        # 补充生成记录登录状态的token
        payload = jwt_payload_handler(user)
        re_dict["token"] = jwt_encode_handler(payload)
        re_dict["name"] = user.name if user.name else user.username
        headers = self.get_success_headers(serializer.data)
        return Response(re_dict, status=status.HTTP_201_CREATED, headers=headers)
    def perform_create(self, serializer):
        return serializer.save()
    #get_permissions 动态权限分配
    #用户注册的时候不应该有权限控制
    #当想获取用户详情信息的时候，必须登录才行
    def get_permissions(self):
        if self.action == "retrieve":
            return [permissions.IsAuthenticated()]
        elif self.action == "create":
            return []
        return []
    #get_serializer_class  动态序列化分配
    #1.UserRegSerializer(用户注册)，只返回username和mobile，会员中心页面需要显示更多字段，所以要创建一个UserDetailSerializer
    #2.问题又来了，如果注册的使用UserDetailSerializer.又导致验证失败，所以需要动态使用serializer
    def get_serializer_class(self):
        print(102,self.action)
        if self.action == 'retrieve':
            return UserDetailSerializer
        elif self.action == 'create':
            return UserRegSerializer
        return UserDetailSerializer
    #虽然继承了Retrieve可以获取用户详情，但是并不知道用户的id，所以要重写get_objece的方法
    #重写get_object方法，就知道哪个是用户,获取登录用户
    def get_object(self):
        return self.request.user