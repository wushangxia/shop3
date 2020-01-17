from django.shortcuts import render
from django.views.generic import View
from goods.models import Goods,GoodsCategory
from goods.serializers import GoodsSerializer,CategorySerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import mixins
from rest_framework import viewsets
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from .filters import GoodFilter
# Create your views here.

# class GoodsListView(View):
#     def get(self,request):
#         json_list = []
#         goods = Goods.objects.all()
#         # for good in goods:
#         #     json_dict ={}
#         #     json_dict['name'] = good.name
#         #     json_dict['category'] = good.category.name
#         #     json_dict['market_price'] = good.market_price
#         #     json_list.append(json_dict)
#         # from django.forms.models import model_to_dict
#         # for good in goods:
#         #     json_dict = model_to_dict(good)
#         #     json_list.append(json_dict)
#         import json
#         from django.core import serializers
#         from django.http import JsonResponse
#         json_data = serializers.serialize('json',goods)
#         json_data = json.loads(json_data)
#         return JsonResponse(json_data,safe=False)

# class GoodsListView(APIView):
#     def get(self,request,format=None):
#         goods = Goods.objects.all()
#         goods_serialzer = GoodsSerializer(goods,many=True)
#         return  Response(goods_serialzer.data)

# class GoodsListView(mixins.ListModelMixin,generics.GenericAPIView):
#     "商品列表页"
#     queryset = Goods.objects.all()
#     serializer_class = GoodsSerializer
#     def get(self,request,*args,**kwargs):
#         return self.list(request,*args,**kwargs)

class GoodsPagination(PageNumberPagination):
    "商品列表自定义分页"
    page_size = 10
    page_size_query_param = "page_size"
    page_query_param =  'page'
    max_page_size = 100

#class GoodsListView(generics.ListAPIView):
    # "商品列表页"
    # pagination_class =  GoodsPagination
    # queryset = Goods.objects.all().order_by('id')
    # serializer_class = GoodsSerializer

class GoodsListViewSet(mixins.ListModelMixin,viewsets.GenericViewSet):
    "商品列表页"
    pagination_class =  GoodsPagination
    queryset = Goods.objects.all().order_by('id')
    serializer_class = GoodsSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_class = GoodFilter

class CategoryViewSet(mixins.ListModelMixin,mixins.RetrieveModelMixin,viewsets.GenericViewSet):
    queryset = GoodsCategory.objects.filter(category_type=1)
    serializer_class = CategorySerializer