from django.shortcuts import render
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q
from rest_framework.mixins import CreateModelMixin
from rest_framework import viewsets
from .serializers import SmsSerializer
from rest_framework.response import Response
from rest_framework import status
from utils.yunpian import YunPian
from shop3.settings import APIKEY
from random import choice
from .models import VerifyCode

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
        mobile = serializer.validated_data('mobile')
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