import django_filters
from .models import Goods
class GoodFilter(django_filters.rest_framework.FilterSet):
    "商品过滤的类"
    price_min = django_filters.NumberFilter(field_name="shop_price",lookup_expr='gte')
    price_max = django_filters.NumberFilter(field_name="shop_price",lookup_expr='lte')
    search_field = django_filters.CharFilter(field_name='name', lookup_expr='contains')
    ordering = django_filters.OrderingFilter(fields=('sold_num', 'add_time'),
                                             field_labels={'sold_num': '销量', 'add_time': '添加时间'})
    class Meta:
        model = Goods
        fields = ['price_min','price_max']