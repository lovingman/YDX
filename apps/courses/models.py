from datetime import datetime

from django.db import models
from DjangoUeditor.models import UEditorField
from teachers.models import Teacher
from users.models import UserProfile


# 课程

class Category(models.Model):
    """
    商品类别
    """
    CATEGORY_TYPE = (
        (1, "方向"),
        (2, "分类"),
        (3, "类型"),
    )

    name = models.CharField(default="", max_length=30, verbose_name="类别名", help_text="类别名")
    code = models.CharField(default="", max_length=30, verbose_name="类别code", help_text="类别code")
    desc = models.TextField(default="", verbose_name="类别描述", help_text="类别描述")
    category_type = models.IntegerField(choices=CATEGORY_TYPE, verbose_name="类目级别")
    parent_category = models.ForeignKey("self", null=True, blank=True, verbose_name="父类目级别", help_text="父目录",
                                        related_name="sub_cat")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "课程类别"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Course(models.Model):
    course_category = models.ForeignKey(Category, verbose_name='课程分类', null=True, blank=True)
    IS_EASY = (('cj', '初级'), ('zj', '中级'), ('gj', '高级'))
    COURSE_TYPE = (
        (1, "基础"),
        (2, "案例"),
        (3, "架构"),
        (4, "工具"),)
    course_type = models.IntegerField(choices=COURSE_TYPE, verbose_name="类型", null=True, blank=True)
    name = models.CharField(max_length=52, verbose_name='课程名字')
    abstract = models.CharField(max_length=50, null=True, blank=True, verbose_name=u"简述");
    price = models.IntegerField(default=0, verbose_name=u"价格");
    desc = models.TextField(max_length=200, null=True, blank=True, verbose_name='课程描述')
    teacher = models.ForeignKey(Teacher, verbose_name='讲师', null=True, blank=True)
    detail = UEditorField(verbose_name='课程详情', width=600, height=300, toolbars="full", imagePath="course/ueditor/",
                          null=True, blank=True, filePath="course/ueditor/", upload_settings={"imageMaxSize": 1204000},
                          default='')
    is_easy = models.CharField(choices=IS_EASY, max_length=2, verbose_name='难度')
    learn_times = models.FloatField(default=0, verbose_name='学习时长(分钟数)')
    students = models.IntegerField(default=0, verbose_name='学习人数')
    fav_nums = models.IntegerField(default=0, verbose_name='收藏人数')
    image = models.ImageField(upload_to='courses/%Y/%m', verbose_name='封面图', max_length=100, null=True, blank=True)
    fight_image = models.ImageField(upload_to='fights/%Y/%m', verbose_name='实战封面图', max_length=100, null=True,
                                    blank=True)
    click_nums = models.IntegerField(default=0, verbose_name='点击数')
    is_banner = models.BooleanField(default=False, verbose_name=u'是否是轮播图')
    is_fight = models.BooleanField(default=False, verbose_name=u"是否实战");
    abstract = models.CharField(max_length=50, null=True, blank=True, verbose_name=u"简述");
    price = models.IntegerField(default=0, verbose_name=u"价格");
    category = models.CharField(default='后端', null=True, blank=True, max_length=20, verbose_name='课程类别')
    tag = models.CharField(default='', verbose_name='课程标签', max_length=10, null=True, blank=True)
    youneed_konw = UEditorField(verbose_name='课程须知', width=600, height=300, toolbars="full",
                                imagePath="course/ueditor/",
                                null=True, blank=True, filePath="course/ueditor/",
                                upload_settings={"imageMaxSize": 1204000},
                                default='')
    teacher_tell = UEditorField(verbose_name='老师能告诉你', width=600, height=300, toolbars="full",
                                imagePath="course/ueditor/",
                                null=True, blank=True, filePath="course/ueditor/",
                                upload_settings={"imageMaxSize": 1204000},
                                default='')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = '课程'
        verbose_name_plural = verbose_name

    def get_zj_nums(self):
        return self.lesson_set.all().count()

    def get_learn_users(self):
        return self.usercourse_set.all()[:5]

    def get_course_lesson(self):
        return self.lesson_set.all()

    def __str__(self):
        return self.name


class BannerCourse(Course):
    class Meta:
        verbose_name = u'轮播课程'
        verbose_name_plural = verbose_name
        proxy = True


class FigthCourse(Course):
    class Meta:
        verbose_name = u'实战课程'
        verbose_name_plural = verbose_name
        proxy = True


# 章节信息


class Lesson(models.Model):
    course = models.ForeignKey(Course, verbose_name='课程')
    name = models.CharField(max_length=100, verbose_name='章节名')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = '章节'
        verbose_name_plural = verbose_name

    def get_lesson_video(self):
        return self.video_set.all()

    def __str__(self):
        return self.name


class Video(models.Model):
    lesson = models.ForeignKey(Lesson, verbose_name='章节')
    name = models.CharField(max_length=100, verbose_name='视频名')
    url = models.URLField(max_length=200, verbose_name='访问地址', default='www.baidu.com')
    learn_times = models.FloatField(default=0, verbose_name='视频时长(分钟数)')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = '视频'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
    def get_lesson(self):
        return self.lesson_set.all()

class CourseProgess(models.Model):
    video=models.ForeignKey(Video,verbose_name="视频id",null=True, blank=True)
    user =models.ForeignKey(UserProfile,verbose_name="用户id",null=True, blank=True)
    progess=models.FloatField(default=0,verbose_name="当前学习时间")
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')
    is_finish=models.BooleanField(default=False,verbose_name="是否看完")
    class Meta:
        verbose_name = '视频进度'
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.video.name
    def get_course_id(self):
        return self.video.lesson.course.id


class CourseResource(models.Model):
    course = models.ForeignKey(Course, verbose_name='课程')
    name = models.CharField(max_length=100, verbose_name='课件名')
    download = models.FileField(upload_to='course/resource/%Y/%m', verbose_name='资源文件', max_length=100)
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')
    class Meta:
        verbose_name = u'课程资源'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


