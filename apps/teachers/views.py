from django.shortcuts import render
from django.views import View
from django.http import HttpResponse
from teachers.models import Teacher
from operation.models import UserFavorite



# Create your views here.
class TeacherDetailView(View):
    def get(self, request,teacher_id):
        teacher = Teacher.objects.get(id=int(teacher_id))
        teacher.click_nums += 1
        teacher.save()
        all_course = teacher.course_set.all()

        # 排行榜讲师
        has_fav_teacher = False
        if not request.user:
            if UserFavorite.objects.filter(user=request.user, fav_id=teacher_id, fav_type=1):
                has_fav_teacher = True


        return render(request,"teacher-center.html", {
            "teacher": teacher,
            "all_course": all_course,
            'has_fav_teacher':has_fav_teacher
        })

