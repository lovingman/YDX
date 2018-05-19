from django.shortcuts import render, render_to_response
from django.views.generic.base import View
from django.http import HttpResponseRedirect, HttpResponse
from courses.models import Course, Category, Video, Lesson,CourseProgess,CourseResource
from users.models import UserProfile
from django.db.models import Q
from teachers.models import Teacher
from django.urls import reverse
from operation.models import UserFavorite, UserCourse, CourseComments
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from utils.mymixin import LoginRequiredMixin
from datetime import datetime


# Create your views here.

class CourseListView(View):
    def get(self, request):
        category_code = request.GET.get('category_code', '')
        all_course = Course.objects.filter(is_fight=False);
        category_type1 = Category.objects.filter(category_type=1)
        category_type2 = Category.objects.filter(category_type=2)

        category_parent_code = ''
        if category_code:
            category_type = Category.objects.filter(code=category_code).filter(category_type=1)
            category_parent_id = Category.objects.get(code=category_code).parent_category_id
            category_parent_code = Category.objects.get(code=category_code).parent_category
            if category_type:
                category_type2 = category_type2.filter(parent_category__code=category_code)
                all_course = all_course.filter(course_category__parent_category__code=category_code)
            else:
                all_course = all_course.filter(course_category__code=category_code)
                category_type2 = category_type2.filter(parent_category=category_parent_id)
        sort = request.GET.get('sort', "")
        is_easy = request.GET.get('is_easy', "")
        type = request.GET.get('type', '')

        if type:
            all_course = all_course.filter(course_type=int(type))
        if sort:
            if sort == "last":
                all_course = all_course.order_by("-add_time")
            elif sort == "pop":
                all_course = all_course.order_by("-click_nums")
        if is_easy:
            if is_easy == 'cj':
                all_course = all_course.filter(is_easy=is_easy)
            elif is_easy == 'zj':
                all_course = all_course.filter(is_easy=is_easy)
            elif is_easy == 'gj':
                all_course = all_course.filter(is_easy=is_easy)
        count = all_course.count()

        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
            # 这里指从all_course中取五个出来，每页显示5个
        p = Paginator(all_course, 5, request=request)
        all_course = p.page(page)

        return render(request, "courses/course-list.html",
                      {
                          'category_type1': category_type1,
                          'category_type2': category_type2,
                          'courses': all_course,
                          'type': type,
                          'sort': sort,
                          'is_easy': is_easy,
                          'category_code': category_code,
                          'parent_code': category_parent_code,
                          'count': count
                      }
                      )




class CourseDetailView(View):
    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))
        lessons = Lesson.objects.filter(course=course).order_by('add_time')
        video = lessons[0].get_lesson_video().order_by('add_time')[0]
        # 课程点击数 + 1
        course.click_nums += 1
        course.save()
        all_comments = CourseComments.objects.filter(course=course).order_by("-add_time")
        # 选出学了这门课的学生关系
        user_courses = UserCourse.objects.filter(course=course)
        # 从关系中取出user_id
        user_ids = [user_course.user_id for user_course in user_courses]
        # 这些用户学了的课程,外键会自动有id，取到字段
        all_user_courses = UserCourse.objects.filter(user_id__in=user_ids)
        # 取出所有课程id
        course_ids = [user_course.course_id for user_course in all_user_courses]
        # 获取学过该课程用户学过的其他课程
        all_learn_course = Course.objects.filter(id__in=course_ids).order_by("-click_nums").exclude(id=course.id)[:4]
        # 找到相关课程
        tag = course.course_category
        relate_courses = []
        if tag:
            relate_courses = Course.objects.filter(course_category=tag)[1:3]

        # 是否收藏课程
        has_fav_course = False
        has_learn_course = False
        progesses = 0
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=course.id, fav_type=1):
                has_fav_course = True
            if UserCourse.objects.filter(user=request.user, course=course):
                has_learn_course = True
            progesses=CourseProgess.objects.filter(user=request.user,video__lesson__course=course)
            if progesses:
                video=progesses.order_by("-add_time")[0].video
        all_resources = CourseResource.objects.filter(course=course)
        return render(request, "courses/course-details.html",
                      {
                          'course': course,
                          'lessons': lessons,
                          'video': video,
                          'progesses':progesses,
                          'all_resources':all_resources,
                          'relate_courses': relate_courses,
                          'all_learn_course': all_learn_course,
                          "all_comments": all_comments,
                          'has_fav_course': has_fav_course,
                          'has_learn_course': has_learn_course
                      })


class FightDetailView(LoginRequiredMixin, View):
    redirect_field_name = 'next'
    def get(self, request, course_id):
        fight = Course.objects.get(id=int(course_id))
        if UserCourse.objects.filter(user=request.user, course=fight):
            lessons = Lesson.objects.filter(course=fight).order_by('add_time')
            if lessons:
                video = lessons[0].get_lesson_video().order_by('add_time')[0]
            # 课程点击数 + 1
            fight.click_nums += 1
            fight.save()
            all_comments = CourseComments.objects.filter(course=fight).order_by("-add_time")
            # 选出学了这门课的学生关系
            user_courses = UserCourse.objects.filter(course=fight, course__is_fight=True)
            # 从关系中取出user_id
            user_ids = [user_course.user_id for user_course in user_courses]
            # 这些用户学了的课程,外键会自动有id，取到字段
            all_user_courses = UserCourse.objects.filter(user_id__in=user_ids)
            # 取出所有课程id
            course_ids = [user_course.course_id for user_course in all_user_courses]
            # 获取学过该课程用户学过的其他课程
            all_learn_course = Course.objects.filter(id__in=course_ids).order_by("-click_nums").exclude(id=fight.id)[:4]
            # 找到相关课程
            tag = fight.course_category
            relate_courses = []
            if tag:
                relate_courses = Course.objects.filter(course_category=tag)[1:3]

            # 是否收藏课程
            has_fav_course = False
            has_learn_course = False
            if request.user.is_authenticated:
                if UserFavorite.objects.filter(user=request.user, fav_id=fight.id, fav_type=1):
                    has_fav_course = True
                if UserCourse.objects.filter(user=request.user, course=fight):
                    has_learn_course = True
                progesses = CourseProgess.objects.filter(user=request.user, video__lesson__course=fight)
                if progesses:
                    video = progesses.order_by("-add_time")[0].video
            all_resources = CourseResource.objects.filter(course=fight)
            return render(request, "courses/course-details.html",
                          {
                              'course': fight,
                              'lessons': lessons,
                              'video': video,
                              'progesses': progesses,
                              'all_resources':all_resources,
                              'relate_courses': relate_courses,
                              'all_learn_course': all_learn_course,
                              "all_comments": all_comments,
                              'has_fav_course': has_fav_course,
                              'has_learn_course': has_learn_course
                          })

class AddFavoriteView(View):
    def post(self, request):
        id = request.POST.get('fav_id', 0)
        type = request.POST.get('fav_type', 0)
        if not request.user.is_authenticated:
            # 未登录时返回json提示未登录，跳转到登录页面是在ajax中做的
            return HttpResponse('{"status":"fail", "msg":"用户未登录"}', content_type='application/json')
        exist_records = UserFavorite.objects.filter(user=request.user, fav_id=int(id), fav_type=int(type))

        if exist_records:
            exist_records.delete()
            if int(type) == 1:
                course = Course.objects.get(id=int(id))
                course.fav_nums -= 1
                if course.fav_nums < 0:
                    course.fav_nums = 0
                course.save()
            elif int(type) == 2:
                teacher = Teacher.objects.get(id=int(id))
                teacher.fav_nums -= 1
                if teacher.fav_nums < 0:
                    teacher.fav_nums = 0
                teacher.save()

            return HttpResponse('{"status":"success", "msg":"收藏"}', content_type='application/json')
        else:
            user_fav = UserFavorite()
            if int(type) > 0 and int(id) > 0:
                user_fav.fav_id = int(id)
                user_fav.fav_type = int(type)
                user_fav.user = request.user
                user_fav.save()
                if int(type) == 1:
                    course = Course.objects.get(id=int(id))
                    course.fav_nums += 1
                    course.save()
                elif int(type) == 2:
                    teacher = Teacher.objects.get(id=int(id))
                    teacher.fav_nums += 1
                    teacher.save()
                return HttpResponse('{"status":"success", "msg":"已收藏"}', content_type='application/json')
            else:
                return HttpResponse('{"status":"fail", "msg":"收藏出错"}', content_type='application/json')


class VideoPlayView(LoginRequiredMixin, View):
    redirect_field_name = 'next'
    def get(self, request, video_id):
        video = Video.objects.get(id=int(video_id))
        course = video.lesson.course
        if course.is_fight:
            user_courses = UserCourse.objects.filter(user=request.user, course=course)
            if not user_courses:
                return HttpResponseRedirect(reverse("index"))
        else:
            user_courses = UserCourse.objects.filter(user=request.user, course=course)
            if not user_courses:
                user_course = UserCourse(user=request.user, course=course)
                user_course.save()
                course.students += 1
                course.save()
        progess=0
        p = CourseProgess.objects.filter(user=request.user, video=video)
        if p:
            progess=int(p[0].progess)
        progesses = CourseProgess.objects.filter(user=request.user, video__lesson__course=course)
        return render(request, "courses/course-video.html", {
            "course": course,
            "video": video,
            "progess":progess,
            "progesses":progesses
        })


class CommentsView(View):
    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))
        progesses=[]
        if course.is_fight:
            if request.user.is_authenticated:
                user_courses = UserCourse.objects.filter(user=request.user, course=course)
                if not user_courses:
                    return HttpResponseRedirect(reverse("index"))
                else:
                    lessons = Lesson.objects.filter(course=course).order_by('add_time')
                    if lessons:
                        video = lessons[0].get_lesson_video().order_by('add_time')
            else:
                return HttpResponseRedirect(reverse("users:login"))
        elif not course.is_fight:
            lessons = Lesson.objects.filter(course=course).order_by('add_time')
            if lessons:
                video = lessons[0].get_lesson_video().order_by('add_time')
        # 课程点击数 + 1
        course.click_nums += 1
        course.save()
        all_comments = CourseComments.objects.filter(course=course).order_by("-add_time")
        # 选出学了这门课的学生关系
        user_courses = UserCourse.objects.filter(course=course)
        # 从关系中取出user_id
        user_ids = [user_course.user_id for user_course in user_courses]
        # 这些用户学了的课程,外键会自动有id，取到字段
        all_user_courses = UserCourse.objects.filter(user_id__in=user_ids)
        # 取出所有课程id
        course_ids = [user_course.course_id for user_course in all_user_courses]
        # 获取学过该课程用户学过的其他课程
        all_learn_course = Course.objects.filter(id__in=course_ids).order_by("-click_nums").exclude(id=course.id)[:4]
        # 找到相关课程
        tag = course.course_category
        relate_courses = []
        if tag:
            relate_courses = Course.objects.filter(course_category=tag)[1:3]

        # 是否收藏课程
        has_fav_course = False
        has_learn_course = False

        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=course.id, fav_type=1):
                has_fav_course = True
            if UserCourse.objects.filter(user=request.user, course=course):
                has_learn_course = True
            progesses = CourseProgess.objects.filter(user=request.user, video__lesson__course=course)
            if progesses:
                video= progesses.order_by("-add_time")[0].video
        return render(request, "courses/course-comment.html",
                      {
                          'course': course,
                          'lessons': lessons,
                          'video': video,
                          'progesses':progesses,
                          'relate_courses': relate_courses,
                          'all_learn_course': all_learn_course,
                          "all_comments": all_comments,
                          'has_fav_course': has_fav_course,
                          'has_learn_course': has_learn_course
                      })

class AddCommentsView(View):
    def post(self, request):
        if not request.user.is_authenticated:
            # 未登录时返回json提示未登录，跳转到登录页面是在ajax中做的
            return HttpResponse('{"status":"fail", "msg":"用户未登录"}', content_type='application/json')
        course_id = request.POST.get("course_id", 0)
        comments = request.POST.get("comments", "")
        if int(course_id) > 0 and comments:
            course_comments = CourseComments()
            # get只能取出一条数据，如果有多条抛出异常。没有数据也抛异常
            # filter取一个列表出来，queryset。没有数据返回空的queryset不会抛异常
            course = Course.objects.get(id=int(course_id))
            # 外键存入要存入对象
            course_comments.course = course
            course_comments.comments = comments
            course_comments.user = request.user
            course_comments.save()
            return HttpResponse('{"status":"success", "msg":"评论成功"}', content_type='application/json',
                                )
        else:
            return HttpResponse('{"status":"fail", "msg":"评论"}', content_type='application/json')


class SearchView(View):
    """
    课程s
    """
    def get(self, request):
        key_words = request.GET.get('words', "");
        sort = request.GET.get('sort', "");
        nums = 0

        if key_words:
            all_course = Course.objects.filter(Q(name__icontains=key_words) | Q(abstract__icontains=key_words))
            if sort == "fight":
                all_course = all_course.filter(is_fight=True).all()
            elif sort == "free":
                all_course = all_course.filter(is_fight=False).all()
            if all_course:
                nums = all_course.count()
                return render(request, 'courses/search.html', {
                    "all_course": all_course,
                    "nums": nums,
                    "words": key_words,
                    "sort": sort
                })
        return render(request, 'courses/search.html', {

            "nums": nums
        })

    def post(self, request):
        key_words = request.POST.get('words', "").replace(' ', '');
        sort = "all"
        nums = 0
        if key_words:
            all_course = Course.objects.filter(Q(name__icontains=key_words) | Q(abstract__icontains=key_words))
            if all_course:
                nums = all_course.count()
                return render(request, 'courses/search.html', {
                    "all_course": all_course,
                    "nums": nums,
                    "words": key_words,

                })
        return render(request, 'courses/search.html', {
            "nums": nums,
        })


class CourseProgessView(View):
    def post(self,request):
        video_id=request.POST.get("video_id")
        whereYouAt=request.POST.get("whereYouAt")
        howLongIsThis=request.POST.get("howLongIsThis")
        print(whereYouAt+"w维王"+howLongIsThis)
        video=Video.objects.get(id=int(video_id))
        video.learn_times=howLongIsThis
        video.save()
        is_finish=False
        if float(whereYouAt)/float(video.learn_times)==1:
            is_finish=True
        course_progess=CourseProgess.objects.filter(user=request.user,video=video)
        if course_progess:
            for progess in course_progess:
                progess.progess=whereYouAt
                print(progess.progess)
                if not progess.is_finish:
                    progess.is_finish=is_finish
                progess.save()
        if not course_progess:
            course_progess = CourseProgess(user=request.user, video=video, progess=whereYouAt,is_finish=is_finish)
            course_progess.save()
        return HttpResponse('{"status":"success", "msg":"成功"}', content_type='application/json',
                            )

class AddCourseNoteView(View):
    def get(self,request):
        pass
    def post(self,request):
        pass

# class CourseNoteListView(View):
#     def get(self,request):
#         pass


