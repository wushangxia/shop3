import xadmin
from xadmin import  views
from .models import VerifyCode

class BaseSetting(object):
    enable_themes = True
    use_bootswatch = True #企图调出主题菜单，显示更多主题

class GlobalSettings(object):
    site_title = "shop3 后台"
    site_footer = "updown"

class VerifyCodeAdmin(object):
    list_display = ["code",'mobile','add_time']

#BaseAdminView: 所有 AdminView 的基础类，注册在该 View 上的插件可以影响所有的 AdminView
#CommAdminView: 用户已经登陆后显示的 View，也是所有登陆后 View 的基础类。该 View主要作用是创建了 Xadmin 的通用元素，例如：系统菜单，用户信息等。插件可以通过注册该 View 来修改这些信息。
#ModelAdminView: 基于 Model 的 AdminView 的基础类，注册的插件可以影响所有基于 Model 的 View。
#ListAdminView: Model 列表页面 View。
#ModelFormAdminView: Model 编辑页面 View。
#CreateAdminView: Model 创建页面 View。
#UpdateAdminView: Model 修改页面 View。
#DeleteAdminView: Model 删除页面 View。
#DetailAdminView: Model 详情页面 View。
xadmin.site.register(VerifyCode,VerifyCodeAdmin)
xadmin.site.register(views.BaseAdminView,BaseSetting)
xadmin.site.register(views.CommAdminView,GlobalSettings)
