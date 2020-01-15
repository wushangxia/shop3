from django.db import models

# Create your models here.
from datetime import datetime
from django.db import models
from django.contrib.auth.models import AbstractUser

class UserProfile(AbstractUser):
    """用户信息"""
    #blank如果为True时django的 Admin 中添加数据时可允许空值，可以不填
    name = models.CharField(max_length=30, null=True, blank=True, verbose_name="姓名")
    birthday = models.DateField(null=True, blank=True, verbose_name="出生年月")
    gender = models.CharField(max_length=6, choices=(("male", u"男"), ("female", "女")), default="female",
                              verbose_name="性别")
    mobile = models.CharField(null=True, blank=True, max_length=11, verbose_name="电话")
    email = models.EmailField(max_length=100, null=True, blank=True, verbose_name="邮箱")
    class Meta:
        verbose_name = '用户信息'
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.username

class VerifyCode(models.Model):
    code = models.CharField('验证码',max_length=10)
    mobile = models.CharField('电话',max_length=11)
    add_time = models.DateTimeField('添加时间',default=datetime.now)
    class Meta:
        verbose_name ="短信验证"
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.code