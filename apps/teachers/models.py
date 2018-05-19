from datetime import datetime
from django.db import models

# Create your models here.


class Teacher(models.Model):

    name = models.CharField(max_length=50, verbose_name='教师名字')
    work_years = models.IntegerField(default=0, verbose_name='工作年限')
    work_company = models.CharField(max_length=50, verbose_name='就职公司')
    work_position = models.CharField(max_length=50, verbose_name='公司职位')
    points = models.CharField(max_length=50, verbose_name='教学特点')
    click_nums = models.IntegerField(default=0, verbose_name='点击数')
    fav_nums = models.IntegerField(default=0, verbose_name='收藏数')
    age = models.IntegerField(default=30, verbose_name='年龄')
    image = models.ImageField(default='', upload_to='teacher/%Y/%m', verbose_name='头像', max_length=100)
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = '教师'
        verbose_name_plural = verbose_name

    def get_course_nums(self):
        return self.course_set.all().count()

    def __str__(self):
        return self.name
