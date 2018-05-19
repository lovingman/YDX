from datetime import datetime
from django.db import models
from DjangoUeditor.models import UEditorField
from users.models import UserProfile
from courses.models import Course, Video


# Create your models here.


class CourseComments(models.Model):
    user = models.ForeignKey(UserProfile, verbose_name='用户')
    course = models.ForeignKey(Course, verbose_name='课程')
    comments = models.CharField(max_length=200, verbose_name='评论')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = '课程评论'
        verbose_name_plural = verbose_name


class UserFavorite(models.Model):
    user = models.ForeignKey(UserProfile, verbose_name='用户')
    # ID 是课程的 ID 或者是 讲师、课程机构的 ID
    fav_id = models.IntegerField(default=0, verbose_name='收藏数据 Id')
    fav_type = models.IntegerField(choices=((1, '课程'), (2, '讲师')), default=1, verbose_name='收藏类型')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = '用户收藏'
        verbose_name_plural = verbose_name


class UserCourse(models.Model):
    user = models.ForeignKey(UserProfile, verbose_name='用户')
    course = models.ForeignKey(Course, verbose_name='课程')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = '用户学习过的课程'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.user.username


class UserNote(models.Model):
    user = models.ForeignKey(UserProfile, verbose_name='用户')
    video = models.ForeignKey(Video, verbose_name="视频id")
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')
    note = UEditorField(verbose_name='笔记', width=600, height=300, toolbars="full", imagePath="course/ueditor/note",
                        null=True, blank=True, filePath="course/ueditor/note",
                        upload_settings={"imageMaxSize": 1204000},
                        default='')

    class Meta:
        verbose_name = '同学笔记'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.user.username
