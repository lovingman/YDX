
# _*_ encoding:utf-8 _*_
import xadmin
from xadmin import views
from xadmin.plugins.auth import UserAdmin
from .models import UserProfile,EmailVerifyRecord,Banner
from trade.models import Order,OrderDetail,Cart
from teachers.models import Teacher
from courses.models import Course,Category,Lesson,Video


__author__ = 'YZF'
__date__ = '2018/3/14,13:59'


# ----- adminx 全局配置


class BaseSetting:
    enable_themes = True
    use_bootswatch = True


class GlobalSettings:
    site_title = '云导学后台管理系统'
    site_footer = '云导学'
    global_models_icon = {
        UserProfile: "glyphicon glyphicon-user",Order:'glyphicon glyphicon-shopping-cart',
        OrderDetail:'glyphicon glyphicon-shopping-cart',Cart:'glyphicon glyphicon-shopping-cart',
        Teacher:'glyphicon glyphicon-star-empty',Course:'glyphicon glyphicon-book',Lesson:'glyphicon glyphicon-book',
        Video:'glyphicon glyphicon-book',
        Category:'glyphicon glyphicon-book'
    }  # 设
    menu_style = 'accordion'

# ------


class EmailVerifyRecordAdmin:
    pass


class BannerAdmin:
    pass


xadmin.site.register(EmailVerifyRecord,EmailVerifyRecordAdmin)
xadmin.site.register(Banner,BannerAdmin)
xadmin.site.register(views.BaseAdminView,BaseSetting)
xadmin.site.register(views.CommAdminView,GlobalSettings)

