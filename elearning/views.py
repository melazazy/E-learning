from django.db.models import Count, Q

from lib2to3.pgen2.token import GREATER
import json
from django.core.serializers.json import DjangoJSONEncoder
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.db.models import Sum, Prefetch
from elearning.serializers import *

# url_Check
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError


from .models import *
from .forms import *


# Create your views here.


def index(request):
    register = userForm(request.POST)
    courses = Course.objects.all().annotate(rates=Sum('students__rate_scale'), raters=Count('students__rate_scale')).prefetch_related(
        'students', 'lectures', 'lessons')
    return render(request, "elearning/index.html", {
        'courses': courses,
        'message': '',
    })


@csrf_exempt
@login_required(login_url='login')  # redirect when user is not logged in
def enroll(request, id):
    ctype = 'free'
    course = Course.objects.get(course_id=id)
    if course.price > 0:
        ctype = 'paid'
    print(ctype)
    u_id = request.user.id
    if Enroll.objects.filter(course_id=id, username=u_id):
        message = "You have Already Enrolling in this course"
        return render(request, "elearning/course.html", {
            'id': id,
            'message': message,
            'course': course,
        })
    if request.method == "POST":
        u_id = request.user.id
        p_type = request.POST.get('type')
        enroll = Course.objects.filter(course_id=id)
        user = User.objects.filter(id=u_id)
        add = Enroll.objects.create(complete_status=False)
        if ctype == 'paid':
            if p_type == 'visa' and request.POST['cardvalue'] == '4121756537315570':
                add.payment_type = p_type
            elif p_type == 'paypal' and request.POST.get('payaccount') == 'admin@example.com':
                add.payment_type = p_type
        elif p_type == 'free':
            add.payment_type = p_type
        add.username.set(user)
        add.course_id.set(enroll)
        add.save()
        lectures = Lecture.objects.filter(course_id=id).first()
        lect = Lecture.objects.filter(
            course_id=id, lecture_id=lectures.lecture_id)
        openstatus = Lessonstatus.objects.create(status=True)
        openstatus.course_id.set(enroll)
        openstatus.lecture_id.set(lect)
        openstatus.student.set(user)
        openstatus.save()
        return HttpResponseRedirect(reverse("index"))

    return render(request, "elearning/enroll.html", {
        'id': id,
        'course': course,
        'type': ctype,
    })


def login_view(request):
    if request.method == "POST":
        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        # Check if authentication successful
        if user is not None:
            login(request, user)
            if 'next' in request.POST:
                return redirect(request.POST['next'])
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "elearning/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "elearning/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        utype = request.POST["type"]
        if password != confirmation:
            return render(request, "elearning/register.html", {
                "message": "Passwords must match."
            })
        if utype == '0':
            return render(request, "elearning/register.html", {
                "message": "Must Select Register As."
            })
        # Attempt to create new user
        try:
            user = User.objects.create_user(
                username, email, password, type=utype)
            user.save()
        except IntegrityError:
            return render(request, "elearning/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "elearning/register.html")


@csrf_exempt
@login_required(login_url='login')
def profile(request, id):
    user = User.objects.filter(pk=id)
    courses = Course.objects.filter(
        teacher__id__in=user).annotate(rates=Sum('students__rate_scale'), raters=Count('students__rate_scale')).prefetch_related(
        'students', 'lectures', 'lessons')
    enroll = Enroll.objects.filter(
        username__id__in=user.all())
    return render(request, 'elearning/profile.html', {
        'id': id,
        'user': user.first(),
        'courses': courses,
        'enroll': enroll,
    })


@csrf_exempt
@login_required(login_url='login')
def editprofile(request, id):
    u_id = request.user.id
    if u_id == id:
        user = User.objects.filter(pk=id).first()
        form = userForm(instance=user)
        if request.method == 'POST':
            form = userForm(request.POST, instance=user)
            form.save()
            return HttpResponseRedirect(reverse("profile", args=(id,)))
        return render(request, 'elearning/editprofile.html', {
            'id': id,
            'form': form,
        })


def course(request, id):
    lastcourse = Course.objects.all().last()
    user = User.objects.filter(pk=request.user.id)
    enrol = Enroll.objects.filter(course_id=id, username__id__in=user)
    if id <= lastcourse.course_id:
        course = Course.objects.filter(course_id=id).annotate(rates=Sum('students__rate_scale'), raters=Count('students__rate_scale')).prefetch_related(
            'students', 'lectures', 'lessons').first()
    else:
        course = ""
    lessons = Lesson.objects.filter(
        course_id=id).exclude(doc_url__isnull=True).exclude(doc_url='').count()
    lectures = Lecture.objects.filter(course_id=id).prefetch_related('lesson')
    comments = Enroll.objects.filter(
        course_id=id).exclude(rate_scale__isnull=True)
    return render(request, "elearning/course.html", {
        'id': id,
        'course': course,
        'lessons': lessons,
        'lectures': lectures,
        'comments': comments,
        'enrol': enrol,
    })


@csrf_exempt
@login_required(login_url='login')
def lectures(request, id):
    u_id = request.user.id
    userobj = User.objects.filter(Q(pk=u_id))
    user = Enroll.objects.filter(course_id=id, username__id__in=userobj)
    leccount = Lecture.objects.filter(course_id=id).count()
    lescount = Lesson.objects.filter(course_id=id).count()
    lesstatus = Lessonstatus.objects.filter(
        course_id=id, student__id__in=userobj).count()
    final = Final_project.objects.filter(course_id=id).first()
    total = 0
    finalstatus = 0
    if final:
        total = (lescount+leccount+1)
    else:
        total = lescount+leccount
    try:
        finalstatus = Final_submission.objects.filter(
            final_id=final.id, user_id__id__in=userobj).count()
    except:
        print(finalstatus)
    status = int((((int(lesstatus)-1) + int(finalstatus))/int(total-1))*100)
    message = ''
    if not user:
        message = 'Only Enrolling Students can watch this courss'
    lectures = Lecture.objects.filter(course_id=id).prefetch_related(
        'discuss', Prefetch('asks', queryset=Questions.objects.filter(lesson_id__isnull=True)), Prefetch('lecturestate', queryset=Lessonstatus.objects.filter(student__id__in=userobj.all())), 'lesson', 'lecture_assignment')

    course = Course.objects.filter(course_id=id).annotate(rates=Sum('students__rate_scale'), raters=Count('students__rate_scale')).prefetch_related(
        'students', 'lectures', 'lessons', 'final').first()
    comments = Enroll.objects.filter(
        course_id=id).exclude(rate_scale__isnull=True)
    grade = Enroll.objects.filter(
        course_id=id, username=u_id, complete_status=True)
    return render(request, "elearning/lecture.html", {
        'id': id,
        'course': course,
        'comments': comments,
        'lectures': lectures,
        'message': message,
        'status': status,
        'grade': grade,
    })


@csrf_exempt
def loadlesson(request):
    u_id = request.user.id
    userobj = User.objects.filter(Q(pk=u_id))
    data = json.loads(request.body)
    course_id = data.get('course_id')
    lecture_id = data.get('lecture_id')
    lesson_id = data.get('lesson_id')
    if lesson_id == 0:
        lectures = Lecture.objects.filter(
            course_id=course_id, lecture_id=lecture_id).prefetch_related('discuss', 'asks', Prefetch('lecturestate', queryset=Lessonstatus.objects.filter(student__id__in=userobj.all()))).all()
        data = lectureSerializer(lectures, many=True).data
        # return JsonResponse(list(data.values()), safe=False)
        return HttpResponse(json.dumps(data, cls=DjangoJSONEncoder), content_type="application/json")
    else:
        lessons = Lesson.objects.filter(
            course_id=course_id, lecture_id=lecture_id, id=lesson_id).prefetch_related('questions', Prefetch('lessonstate', queryset=Lessonstatus.objects.filter(student__id__in=userobj.all()))).all()
        data = lessonsSerializer(lessons, many=True).data
        return HttpResponse(json.dumps(data, cls=DjangoJSONEncoder), content_type="application/json")


@csrf_exempt
def addcomment(request, c_id, l_id):
    u_id = request.user.id
    userobj = User.objects.filter(Q(pk=u_id))
    course = Course.objects.filter(course_id=c_id)
    lecture = Lecture.objects.filter(lecture_id=l_id)
    if request.method == 'POST':
        comment = request.POST.get('comment')
        add = Discussion_board_for_lecture.objects.create(comment=comment)
        add.course_id.set(course)
        add.lecture_id.set(lecture)
        add.user_id.set(userobj)
        add.save()
        return HttpResponseRedirect(reverse("lectures", args=(c_id,)))


@csrf_exempt
def assigne(request):
    u_id = request.user.id
    userobj = User.objects.filter(Q(pk=u_id))
    # loadassign in coures view
    data = json.loads(request.body)
    course_id = data.get('course_id')
    lecture_id = data.get('lecture_id')
    assign = Assignment.objects.filter(
        course_id=course_id, lecture_id=lecture_id).prefetch_related(Prefetch('answers', queryset=Assignment_submission.objects.filter(user_id=u_id)), Prefetch('assignment_status', queryset=Assignment_status.objects.filter(student__id__in=userobj.all()))).all()
    data = assignmentSerializer(assign, many=True).data
    return HttpResponse(json.dumps(data, cls=DjangoJSONEncoder), content_type="application/json")


@csrf_exempt
def filltercourses(request):
    data = json.loads(request.body)
    cat = data.get("cat")
    p = float(data.get("price"))
    fcourses = 0
    # tag__id__in=news.tag.all()
    category = Category.objects.filter(name=cat)
    if p > 0:
        if cat != '0':
            fcourses = Course.objects.filter(categorys__id__in=category.all(), price__gte=p).prefetch_related(
                'students', 'lectures', 'lessons').annotate(rates=Sum('students'))
        else:
            fcourses = Course.objects.filter(price__gte=p).prefetch_related(
                'students', 'lectures', 'lessons').annotate(rates=Sum('students'))
    elif p == 0:
        if cat != '0':
            fcourses = Course.objects.filter(categorys__id__in=category.all(), price=p).prefetch_related(
                'students', 'lectures', 'lessons').annotate(rates=Sum('students'))
        else:
            fcourses = Course.objects.filter(price=p).prefetch_related(
                'students', 'lectures', 'lessons').annotate(rates=Sum('students'))
    else:
        if cat != '0':
            fcourses = Course.objects.filter(categorys__id__in=category.all()).prefetch_related(
                'students', 'lectures', 'lessons').annotate(rates=Sum('students'))
        else:
            fcourses = Course.objects.all().prefetch_related(
                'students', 'lectures', 'lessons').annotate(rates=Sum('students'))

    data = courseSerializer(fcourses, many=True).data
    return HttpResponse(json.dumps(data, cls=DjangoJSONEncoder), content_type="application/json")


@csrf_exempt
@login_required(login_url='login')
def addcourse(request):
    u_id = request.user.id
    user = User.objects.filter(
        Q(pk=u_id, type='Teacher') | Q(pk=u_id, type='Admin'))
    print("user")
    print(user)
    message = ''
    if not user:
        message = 'Only Teachers And Admins can Add Courses'
    if request.method == 'POST':
        form = addcourseForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            addCourse = form.save()
            addCourse.teacher.set(user)
            addCourse.save()
            last = Course.objects.filter(
                teacher=u_id).order_by('course_id').last()
            # addCourse.save_m2m()
            # ...
            # redirect to a new URL:
            return HttpResponseRedirect(reverse("profile", args=(u_id,)))
    else:
        return render(request, "elearning/addcourse.html", {
            'form': addcourseForm(),
            'message': message,
        })
    return render(request, "elearning/addcourse.html", {
        'form': addcourseForm(),
        'message': message,
    })


@csrf_exempt
@login_required(login_url='login')
def editcourse(request, id):
    u_id = request.user.id
    user = User.objects.filter(
        Q(pk=u_id, type='Teacher') | Q(pk=u_id, type='Admin'))
    course = Course.objects.filter(
        course_id=id, teacher__id__in=user.all()).first()
    message = ''
    if not course:
        message = 'Only Teachers And Admins can Edit Courses'
    if request.method == 'POST':
        form = addcourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("manage", args=((id),)))
    else:
        return render(request, "elearning/editcourse.html", {
            'id': id,
            'form': addcourseForm(instance=course),
            'message': message,
        })


@csrf_exempt
@login_required(login_url='login')
def delcourse(request, id):
    u_id = request.user.id
    user = User.objects.filter(
        Q(pk=u_id, type='Teacher') | Q(pk=u_id, type='Admin'))
    course = Course.objects.filter(
        course_id=id, teacher__id__in=user.all()).first()
    message = ''
    if not course:
        message = 'Only Teachers own the course And Admins can Edit Courses'
        return render(request, "elearning/delcourse.html", {
            'id': id,
            'message': message,
        })
    if request.method == 'POST':
        if course:
            course.delete()
            return HttpResponseRedirect(reverse("manage", args=((id),)))
    else:
        return render(request, "elearning/delcourse.html", {
            'id': id,
            'message': message,
            'title': course.course_title,
        })


@csrf_exempt
@login_required(login_url='login')
def addlecture(request):
    u_id = request.user.id
    user = User.objects.filter(
        Q(pk=u_id, type='Teacher') | Q(pk=u_id, type='Admin'))
    courses = Course.objects.filter(teacher__id__in=user.all())
    message = ''
    if not user:
        message = 'Only Teachers And Admins can Add Lectures'
    if request.method == 'POST':
        form = addlectureForm(request.POST)
        if form.is_valid():
            course_id = request.POST.get('course')
            course = Course.objects.filter(course_id=course_id)
            addlecture = form.save()
            addlecture.course_id.set(course)
            addlecture.save()
            return HttpResponseRedirect(reverse("addlecture"))
    else:
        return render(request, "elearning/addlecture.html", {
            'form': addlectureForm(),
            'message': message,
            'courses': courses,
        })


@csrf_exempt
@login_required(login_url='login')
def editlecture(request, cid, lid):
    u_id = request.user.id
    user = User.objects.filter(
        Q(pk=u_id, type='Teacher') | Q(pk=u_id, type='Admin'))
    courses = Course.objects.filter(teacher__id__in=user.all())
    lecture = Lecture.objects.filter(
        course_id__in=courses.all(), lecture_id=lid).first()
    message = ''
    if not lecture:
        message = 'Only Teachers who own this cousre can add or edit lecture'
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = addlectureForm(request.POST, instance=lecture)
        if form.is_valid():
            edit = form.save()
            edit.save()
            return HttpResponseRedirect(reverse("manage", args=((cid),)))
    else:
        return render(request, "elearning/editlecture.html", {
            'cid': cid,
            'lid': lid,
            'form': addlectureForm(instance=lecture),
            'message': message,
            'courses': courses,
        })
    return render(request, "elearning/editlecture.html", {
        'cid': cid,
        'lid': lid,
        'form': addlectureForm(instance=lecture),
        'message': message,
        'courses': courses,
    })


@csrf_exempt
@login_required(login_url='login')
def dellecture(request, cid, lid):
    u_id = request.user.id
    user = User.objects.filter(
        Q(pk=u_id, type='Teacher') | Q(pk=u_id, type='Admin'))
    courses = Course.objects.filter(teacher__id__in=user.all())
    lecture = Lecture.objects.filter(
        course_id__in=courses.all(), lecture_id=lid).first()
    if request.method == 'POST':
        if lecture:
            lecture.delete()
            return HttpResponseRedirect(reverse("manage", args=((cid),)))
    else:
        return HttpResponse('')


@csrf_exempt
def addlecturejson(request):
    # JSON Function
    data = json.loads(request.body)
    course_id = data.get('course_id')
    lectures = Lecture.objects.filter(
        course_id=course_id).prefetch_related('lesson').all()
    data = lectureSerializer(lectures, many=True).data
    return HttpResponse(json.dumps(data, cls=DjangoJSONEncoder), content_type="application/json")


@csrf_exempt
@login_required(login_url='login')
def addlesson(request):
    u_id = request.user.id
    user = User.objects.filter(
        Q(pk=u_id, type='Teacher') | Q(pk=u_id, type='Admin'))
    courses = Course.objects.filter(teacher__id__in=user.all())
    message = ''
    if not user:
        message = 'Only Teachers And Admins can Add Lectures'
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = addlessonForm(request.POST)
        if form.is_valid():
            course_id = request.POST.get('course')
            lecture_id = request.POST.get('lecture')
            course = Course.objects.filter(course_id=course_id)
            lecture = Lecture.objects.filter(lecture_id=lecture_id)
            addlesson = form.save()
            addlesson.course_id.set(course)
            addlesson.lecture_id.set(lecture)
            addlesson.save()
            return HttpResponseRedirect(reverse("manage", args=(course_id,)))
    else:
        return render(request, "elearning/addlesson.html", {
            'form': addlessonForm(),
            'message': message,
            'courses': courses,
        })
    return render(request, "elearning/addlesson.html", {
        'form': addlessonForm(),
        'message': message,
        'courses': courses,
    })


@csrf_exempt
@login_required(login_url='login')
def editlesson(request, cid, lid, lesonid):
    u_id = request.user.id
    user = User.objects.filter(
        Q(pk=u_id, type='Teacher') | Q(pk=u_id, type='Admin'))
    course = Course.objects.filter(course_id=cid, teacher__id__in=user.all())
    lesson = Lesson.objects.filter(
        course_id__in=course.all(), lecture_id=lid, id=lesonid).first()
    message = ''
    if not course:
        message = 'Only Teachers And Admins can Edit Lessons'
    if request.method == 'POST':
        form = addlessonForm(request.POST, instance=lesson)
        if form.is_valid():
            addlesson = form.save()
            addlesson.save()
            return HttpResponseRedirect(reverse("manage", args=((cid),)))
    else:
        return render(request, "elearning/editlesson.html", {
            'cid': cid,
            'lid': lid,
            'lesonid': lesonid,
            'form': addlessonForm(instance=lesson),
            'message': message,
            'courses': course,
        })
    return render(request, "elearning/editlesson.html", {
        'cid': cid,
        'lid': lid,
        'lesonid': lesonid,
        'form': addlessonForm(instance=lesson),
        'message': message,
        'courses': course,
    })


@csrf_exempt
@login_required(login_url='login')
def dellesson(request, cid, lid, lesonid):
    u_id = request.user.id
    user = User.objects.filter(
        Q(pk=u_id, type='Teacher') | Q(pk=u_id, type='Admin'))
    course = Course.objects.filter(course_id=cid, teacher__id__in=user.all())
    lesson = Lesson.objects.filter(
        course_id__in=course.all(), lecture_id=lid, id=lesonid).first()
    if request.method == 'POST':
        if lesson:
            lesson.delete()
            return HttpResponseRedirect(reverse("manage", args=((cid),)))
    else:
        return HttpResponse('NOT Correct')


@csrf_exempt
@login_required(login_url='login')
def addquestion(request):
    u_id = request.user.id
    user = User.objects.filter(
        Q(pk=u_id, type='Teacher') | Q(pk=u_id, type='Admin'))
    courses = Course.objects.filter(teacher__id__in=user.all())
    message = ''
    if not user:
        message = 'Only Teachers And Admins can Add Lectures'
    if request.method == 'POST':
        form = addquestionForm(request.POST)
        if form.is_valid():
            course_id = request.POST.get('course')
            lecture_id = request.POST.get('lecture')
            lesson_id = request.POST.get('lesson')
            lesson = ''
            course = Course.objects.filter(course_id=course_id)
            lecture = Lecture.objects.filter(lecture_id=lecture_id)
            if lesson_id:
                lesson = Lesson.objects.filter(id=lesson_id)
            addq = form.save()
            addq.course_id.set(course)
            addq.lecture_id.set(lecture)
            if lesson:
                addq.lesson_id.set(lesson)
            else:
                addq.lesson_id.set('')
            addq.save()
            return HttpResponseRedirect(reverse("manage", args=(course_id,)))
    else:
        return render(request, "elearning/addquestion.html", {
            'form': addquestionForm(),
            'message': message,
            'courses': courses,
        })
    return render(request, "elearning/addquestion.html", {
        'form': addquestionForm(),
        'message': message,
        'courses': courses,
    })


@csrf_exempt
@login_required(login_url='login')
def editquestion(request, qid):
    u_id = request.user.id
    user = User.objects.filter(
        Q(pk=u_id, type='Teacher') | Q(pk=u_id, type='Admin'))
    course = Course.objects.filter(teacher__id__in=user.all())
    question = Questions.objects.filter(
        course_id__in=course.all(), pk=qid).first()
    courseid = []
    for e in question.course_id.all():
        courseid.append(e.course_id)
    message = ''
    if not question:
        message = 'Only Teachers And Admins can Add Lectures'
    if request.method == 'POST':
        form = addquestionForm(request.POST, instance=question)
        if form.is_valid():
            addq = form.save()
            addq.save()
            return HttpResponseRedirect(reverse("manage", args=(courseid[0],)))
    return render(request, "elearning/editquestion.html", {
        'qid': qid,
        'form': addquestionForm(instance=question),
        'message': message,
        'courses': course,
    })


@csrf_exempt
@login_required(login_url='login')
def delquestion(request, qid):
    u_id = request.user.id
    user = User.objects.filter(
        Q(pk=u_id, type='Teacher') | Q(pk=u_id, type='Admin'))
    course = Course.objects.filter(teacher__id__in=user.all())
    question = Questions.objects.filter(
        course_id__in=course.all(), pk=qid).first()
    courseid = []
    for e in question.course_id.all():
        courseid.append(e.course_id)
    if request.method == 'POST':
        if question:
            question.delete()
            return HttpResponseRedirect(reverse("manage", args=(courseid[0],)))
    else:
        return HttpResponse('NOT Correct')


@csrf_exempt
@login_required(login_url='login')
def addassigne(request):
    u_id = request.user.id
    user = User.objects.filter(
        Q(pk=u_id, type='Teacher') | Q(pk=u_id, type='Admin'))
    courses = Course.objects.filter(teacher__id__in=user.all())
    message = ''
    if not courses:
        message = 'Only Teachers And Admins can Add Lectures'
    if request.method == 'POST':
        form = addassignmentForm(request.POST)
        if form.is_valid():
            course_id = request.POST.get('course')
            lecture_id = request.POST.get('lecture')
            course = Course.objects.filter(course_id=course_id)
            lecture = Lecture.objects.filter(lecture_id=lecture_id)
            addA = form.save()
            addA.course_id.set(course)
            addA.lecture_id.set(lecture)
            addA.save()
            return HttpResponseRedirect(reverse("manage", args=(course_id,)))
    return render(request, "elearning/addassignment.html", {
        'form': addassignmentForm(),
        'message': message,
        'courses': courses,
    })


@csrf_exempt
@login_required(login_url='login')
def editassigne(request, id):
    u_id = request.user.id
    user = User.objects.filter(
        Q(pk=u_id, type='Teacher') | Q(pk=u_id, type='Admin'))
    courses = Course.objects.filter(teacher__id__in=user.all())
    assignement = Assignment.objects.filter(pk=id).first()
    message = ''
    courseid = []
    for e in assignement.course_id.all():
        courseid.append(e.course_id)
    if not courses:
        message = 'Only Teachers And Admins can Edit This Assignment'
    if request.method == 'POST':
        form = addassignmentForm(request.POST, instance=assignement)
        if form.is_valid():
            addA = form.save()
            addA.save()
            return HttpResponseRedirect(reverse("manage", args=(courseid[0],)))
    return render(request, "elearning/editassigne.html", {
        'id': id,
        'form': addassignmentForm(instance=assignement),
        'message': message,
        'courses': courses,
    })


@csrf_exempt
@login_required(login_url='login')
def delassigne(request, id):
    u_id = request.user.id
    user = User.objects.filter(
        Q(pk=u_id, type='Teacher') | Q(pk=u_id, type='Admin'))
    course = Course.objects.filter(teacher__id__in=user.all())
    assignement = Assignment.objects.filter(
        course_id__in=course.all(), pk=id).first()
    courseid = []
    for e in assignement.course_id.all():
        courseid.append(e.course_id)
    if request.method == 'POST':
        if assignement:
            assignement.delete()
            return HttpResponseRedirect(reverse("manage", args=(courseid[0],)))
    else:
        return HttpResponse('NOT Correct')


@csrf_exempt
@login_required(login_url='login')
def managefinal(request, id):
    u_id = request.user.id
    user = User.objects.filter(
        Q(pk=u_id, type='Teacher') | Q(pk=u_id, type='Admin'))
    courses = Course.objects.filter(course_id=id, teacher__id__in=user.all())
    course = Course.objects.filter(course_id=id)
    final = Final_project.objects.filter(course_id__in=courses.all()).first()
    if courses:
        if request.method == 'POST':
            if request.POST.get("button") == "Add":
                print("ADD: ")
                form = addfinalForm(request.POST)
                if form.is_valid():
                    course = Course.objects.filter(course_id=id)
                    addA = form.save()
                    addA.course_id.set(course)
                    addA.save()
                return HttpResponseRedirect(reverse("manage", args=(id,)))
            if request.POST.get("button") == "Edit":
                print("Edit: ")
                form = addfinalForm(request.POST, instance=final)
                if form.is_valid():
                    addA = form.save()
                    addA.save()
                return HttpResponseRedirect(reverse("manage", args=(id,)))
        if final != None:
            print("Final")
            return render(request, "elearning/managefinal.html", {
                'id': id,
                'form': addfinalForm(instance=final),
            })
        else:
            print("Not Final")
            return render(request, "elearning/managefinal.html", {
                'action': 'add',
                'id': id,
                'form': addfinalForm(),
            })
    else:
        return render(request, "elearning/managefinal.html", {
            'id': id,
            'message': 'You Don\'t Have permession to manage This course. ',
        })


@csrf_exempt
@login_required(login_url='login')
def manage(request, id):
    u_id = request.user.id
    course = Course.objects.filter(
        course_id=id, teacher=u_id).prefetch_related('lectures', 'lessons').all()
    # delete final project method
    if course:
        final = Final_project.objects.filter(course_id=id).first()
        if request.method == 'POST':
            if request.POST.get("button") == "Delete":
                if final:
                    final.delete()
                return HttpResponseRedirect(reverse("manage", args=(id,)))
        return render(request, 'elearning/manage.html', {
            'id': id,
            'course': course,
        })
    return render(request, 'elearning/manage.html', {
        'message': "You Can Not Edit This Course",
        'id': id,
        'course': course,
    })


@csrf_exempt
@login_required(login_url='login')
def grade(request, c_id, u_id):
    grade = Grade.objects.filter(course_id=c_id, user_id=u_id).first()
    return render(request, 'elearning/grade.html', {
        'grade': grade,
        'id': id,
    })


@csrf_exempt
@login_required(login_url='login')
def completestatus(request):
    u_id = request.user.id
    userobj = User.objects.filter(Q(pk=u_id))
    data = json.loads(request.body)
    course_id = data.get('course_id')
    lecture_id = data.get('lecture_id')
    lesson_id = data.get('lesson_id')
    course = Course.objects.filter(course_id=course_id)
    lecture = Lecture.objects.filter(lecture_id=lecture_id)
    if lesson_id == 0:
        lesson = Lesson.objects.filter(
            course_id=course_id, lecture_id=lecture_id).first()
        complete = Lessonstatus.objects.filter(
            course_id=course_id, lecture_id=lecture_id, lesson_id=lesson.id, student=u_id)
        if not complete:
            lesson_stat = Lesson.objects.filter(
                course_id=course_id, lecture_id=lecture_id, id=lesson.id)
            add = Lessonstatus.objects.create(status=True)
            add.course_id.set(course)
            add.lecture_id.set(lecture)
            add.lesson_id.set(lesson_stat)
            add.student.set(userobj)
            add.save()
            print("Done:")
            return HttpResponseRedirect(reverse("lectures", args=(course_id,)))
        else:
            print("ACtive")
    else:
        lesson = Lesson.objects.filter(
            course_id=course_id, lecture_id=lecture_id).last()
        if lesson.id == lesson_id:
            # Should compleate next Assignment Status
            complete = Assignment_status.objects.filter(
                course_id=course_id, lecture_id=lecture_id, student=u_id)
            if not complete:
                assign_stat = Assignment.objects.filter(
                    course_id=course_id, lecture_id=lecture_id)
                add = Assignment_status.objects.create(status=True)
                add.course_id.set(course)
                add.lecture_id.set(lecture)
                add.assignment_id.set(assign_stat)
                add.student.set(userobj)
                add.save()
                return HttpResponseRedirect(reverse("lectures", args=(course_id,)))
        else:
            print("Not Last")
            complete = Lessonstatus.objects.filter(
                course_id=course_id, lecture_id=lecture_id, lesson_id=lesson_id+1, student=u_id)
            if not complete:
                lesson_stat = Lesson.objects.filter(
                    course_id=course_id, lecture_id=lecture_id, id=lesson.id)
                add = Lessonstatus.objects.create(status=True)
                add.course_id.set(course)
                add.lecture_id.set(lecture)
                add.lesson_id.set(lesson_stat)
                add.student.set(userobj)
                add.save()
                print("Done: Lesson")
                return HttpResponseRedirect(reverse("lectures", args=(course_id,)))


@csrf_exempt
@login_required(login_url='login')
def loadfinal(request):
    u_id = request.user.id
    data = json.loads(request.body)
    course_id = data.get('course_id')
    final = Final_project.objects.filter(course_id=course_id).prefetch_related(
        Prefetch('submission', queryset=Final_submission.objects.filter(user_id=u_id))).all()
    data = Final_projectSerializer(final, many=True).data
    # return JsonResponse(list(final.values()), safe=False)
    return HttpResponse(json.dumps(data, cls=DjangoJSONEncoder), content_type="application/json")


@csrf_exempt
@login_required(login_url='login')
def submitassigne(request):
    u_id = request.user.id
    user = User.objects.filter(Q(pk=u_id))
    if request.method == 'POST':
        id = request.POST.get("id")
        answer = request.POST.get("answer")
        assignment = Assignment.objects.filter(pk=id)
        c_id = 0
        for a in assignment:
            for c in a.course_id.all():
                c_id = c.course_id

        ass = Assignment_submission.objects.filter(
            assignment_id=id, user_id=u_id)
        if not ass:
            validator = URLValidator()
            try:
                validator(answer)
                add = Assignment_submission.objects.create(answer=answer)
                add.assignment_id.set(assignment)
                add.user_id.set(user)
                add.save()
            except ValidationError as exception:
                print("Incorrect")
    return HttpResponseRedirect(reverse("lectures", args=(c_id,)))


@csrf_exempt
@login_required(login_url='login')
def submitfinal(request):
    u_id = request.user.id
    user = User.objects.filter(Q(pk=u_id))
    if request.method == 'POST':
        id = request.POST.get("id")
        answer = request.POST.get("answer")
        final = Final_project.objects.filter(pk=id)
        c_id = 0
        for a in final:
            for c in a.course_id.all():
                c_id = c.course_id
        assignment = Final_submission.objects.filter(pk=id, user_id=u_id)
        if not assignment:
            validator = URLValidator()
            try:
                validator(answer)
                add = Final_submission.objects.create(answer=answer)
                add.final_id.set(final)
                add.user_id.set(user)
                add.save()
                return HttpResponseRedirect(reverse("lectures", args=(c_id,)))
            except ValidationError as exception:
                print("Incorrect")
                print(exception)
    return HttpResponseRedirect(reverse("lectures", args=(c_id,)))


@csrf_exempt
@login_required(login_url='login')
def gradeassigne(request, a_id, s_id):
    ass = Assignment.objects.filter(Q(pk=a_id))
    sub = Assignment_submission.objects.filter(Q(pk=s_id))
    c_id = ''
    l_id = ''
    user_id = ''
    for a in ass:
        for c in a.course_id.all():
            c_id = c.course_id
        for l in a.lecture_id.all():
            l_id = l.lecture_id
    for u in sub:
        for x in u.user_id.all():
            user_id = x.id
    userobj = User.objects.filter(Q(pk=user_id))
    if request.method == 'POST':
        lastlecture = Lecture.objects.filter(course_id=c_id).last()
        course = Course.objects.filter(course_id=c_id)
        update = Assignment_submission.objects.get(pk=s_id)
        degree = request.POST.get("degree")
        update.grade = degree
        update.save()
        if not lastlecture.lecture_id == l_id:
            lecture = Lecture.objects.filter(course_id=c_id, lecture_id=l_id+1)
            add = Lessonstatus.objects.create(status=True)
            add.course_id.set(course)
            add.lecture_id.set(lecture)
            # add.lesson_id.set(lesson_stat)
            add.student.set(userobj)
            add.save()
        return HttpResponseRedirect(reverse("manage", args=(c_id,)))
    return render(request, 'elearning/gradeassigne.html', {
        'a_id': a_id,
        's_id': s_id,
        'ass': ass,
        'sub': sub,
    })


@csrf_exempt
@login_required(login_url='login')
def gradefinal(request, f_id, fs_id):
    u_id = request.user.id
    final = Final_project.objects.filter(Q(pk=f_id))
    sub = Final_submission.objects.filter(Q(pk=fs_id))
    c_id = ''
    student_id = ''
    for a in final:
        for c in a.course_id.all():
            c_id = c.course_id

    for a in sub:
        for u in a.user_id.all():
            student_id = u.id

    if request.method == 'POST':
        update = Final_submission.objects.get(pk=fs_id)
        degree = request.POST.get("degree")
        update.grade = degree
        update.save()
        if int(degree) >= 50:
            complete = Enroll.objects.get(
                course_id=c_id, username=student_id)
            complete.complete_status = True
            complete.save()
        return HttpResponseRedirect(reverse("manage", args=(c_id,)))
    return render(request, 'elearning/gradefinal.html', {
        'a_id': f_id,
        's_id': fs_id,
        'ass': final,
        'sub': sub,
    })


@csrf_exempt
@login_required(login_url='login')
def upload_cert(request, c_id, u_id):
    form = gradeForm()
    user = User.objects.filter(pk=u_id)
    course = Course.objects.filter(course_id=c_id)
    grade = Grade.objects.filter(course_id=c_id, user_id=u_id)

    if request.method == 'POST':
        if not grade:
            final = Final_project.objects.filter(course_id=c_id).first()
            final_id = Final_submission.objects.filter(final_id=final.pk)
            form = gradeForm(request.POST, request.FILES)
            if form.is_valid():
                print("Valid: ")
                add = form.save()
                add.course_id.set(course)
                add.final_id.set(final_id)
                add.user_id.set(user)
                add.save()
                return HttpResponseRedirect(reverse("manage", args=(c_id,)))
        else:
            return render(request, 'elearning/uploadcert.html', {
                'message': 'This Student Already Have Cert',
                'user': user,
                'course': course,
                'form': form,
            })

    return render(request, 'elearning/uploadcert.html', {
        'user': user,
        'course': course,
        'form': form,
    })


@csrf_exempt
@login_required(login_url='login')
def addreview(request, id):
    u_id = request.user.id
    enroll = Enroll.objects.get(course_id=id, username=u_id)
    if request.method == 'POST':
        if enroll:
            rate = request.POST.get("rate")
            review = request.POST.get("review")
            enroll.rate_scale = rate
            enroll.review = review
            enroll.save()
            return HttpResponseRedirect(reverse("lectures", args=(id,)))
