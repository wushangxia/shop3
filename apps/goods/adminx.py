import xadmin
from .models import Goods,GoodsCategory,GoodsImage,GoodsCategoryBrand,Banner,HotSearchWords
from .models import IndexAd

class GoodsAdmin(object):
    list_display = ["name", "click_num", "sold_num", "fav_num", "goods_num", "market_price",
                    "shop_price", "goods_brief", "goods_desc", "is_new", "is_hot", "add_time"]
    search_fields = ['name',]
    list_editable = ["is_hot", ] # 在列表页可以快速直接编辑的字段
    list_filter = ["name", "click_num", "sold_num", "fav_num", "goods_num", "market_price",
                   "shop_price", "is_new", "is_hot", "add_time", "category__name"]
    style_fields = {"goods_desc": "ueditor"} #控制字段的显示样式
    class GoodsImagesInline(object): #inlines添加数据
        model = GoodsImage
        exclude = ["add_time"]
        extra = 1
        style = "tab"

    inlines = [GoodsImagesInline] #添加数据

class GoodsCategoryAdmin(object):
    list_display = ["name","category_type","parent_category","add_time"]
    list_filter = ["category_type","parent_category","name"]
    search_fields = ["name"]

class GoodsBrandAdmin(object):
    list_display = ["category","image","name","desc"]
    # 实现过滤出所有的一级类目
    def get_context(self):
        context = super(GoodsBrandAdmin,self).get_context()
        if 'from' in context:
            context["from"].fields['category'].queryset = GoodsCategory.objects.filter(category=1)
            return context

class BannerGoodsAdmin(object):
    list_display = ["goods","image","index"]

class HotSearchAdmin(object):
    list_display = ["keywords", "index", "add_time"]

class IndexAdAdmin(object):
    list_display = ["category","goods"]

xadmin.site.register(Goods,GoodsAdmin)
xadmin.site.register(GoodsCategory,GoodsBrandAdmin)
xadmin.site.register(Banner,BannerGoodsAdmin)
xadmin.site.register(GoodsCategoryBrand,GoodsBrandAdmin)
xadmin.site.register(HotSearchWords,HotSearchAdmin)
xadmin.site.register(IndexAd,IndexAdAdmin)

