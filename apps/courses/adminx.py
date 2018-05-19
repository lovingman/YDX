# _*_ encoding:utf-8 _*_
import xadmin
from xadmin import views
from .models import Course, Lesson, Video, Category, BannerCourse, FigthCourse,CourseResource,CourseProgess

__author__ = 'YZF'
__date__ = '2018/3/14,14:23'


class LessonInline:
    model = Lesson
    extra = 0


class VideoInline:
    model = Video
    extra = 0


class CourseAdmin(object):
    list_display = ['name', 'image']
    style_fields = {"detail": "ueditor", "youneed_konw": "ueditor", "teacher_tell": "ueditor", }
    # Inline # 添加课程的时候可以顺便添加章节、课程资源
    inlines = [LessonInline]

    def queryset(self):
        qs = super(CourseAdmin, self).queryset()
        qs = qs.filter(is_banner=False, is_fight=False)
        return qs


class BannerCourseAdmin(object):
    list_display = ['name', 'image']
    style_fields = {"detail": "ueditor", "youneed_konw": "ueditor", "teacher_tell": "ueditor", }
    inlines = [LessonInline]

    def queryset(self):
        qs = super(BannerCourseAdmin, self).queryset()
        qs = qs.filter(is_banner=True)
        return qs


class FightCourseAdmin(object):
    list_display = ['name', 'image']
    style_fields = {"detail": "ueditor", "youneed_konw": "ueditor", "teacher_tell": "ueditor", }
    inlines = [LessonInline]

    def queryset(self):
        qs = super(FightCourseAdmin, self).queryset()
        qs = qs.filter(is_fight=True)
        return qs


class LessonAdmin(object):
    inlines = [VideoInline]


class VideoAdmin(object):
    pass

class CourseResourceAdmin:
    pass
class CourseProgessAdmin:
    pass

class CategoryAdmin(object):
    pass

xadmin.site.register(Course, CourseAdmin)
xadmin.site.register(CourseResource,CourseResourceAdmin)
xadmin.site.register(CourseProgess,CourseProgessAdmin)
xadmin.site.register(BannerCourse, BannerCourseAdmin)
xadmin.site.register(FigthCourse, FightCourseAdmin)
xadmin.site.register(Lesson, LessonAdmin)
xadmin.site.register(Video, VideoAdmin)
xadmin.site.register(Category, CategoryAdmin)
