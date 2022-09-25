from email.mime import image
from email.policy import default
from itertools import count
from pydoc import describe
from turtle import title
from django.db import models
from django.contrib.auth.models import AbstractUser


def from_364():
    '''
    Returns the next default value for the `ones` field,
    starts from 364
    '''
    largest = Course.objects.all().order_by('course_id').last()
    if not largest.course_id:
        return 364
    return largest.course_id + 1

# Create your models here.


class User(AbstractUser):
    cat = (
        ('Student', 'student'),
        ('Teacher', 'teacher'),
        ('Admin', 'admin'),
    )
    type = models.CharField(max_length=200, null=True, choices=cat)
    image = models.URLField(
        null=True, default='https://via.placeholder.com/150x150/FFFF00/000000/?text=User+IMG')

    def __str__(self):
        return f'{self.pk}){self.username}'


class Category(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class Course(models.Model):
    course_id = models.AutoField(primary_key=True, default=from_364)
    course_title = models.CharField(max_length=100)
    describe = models.TextField(max_length=700, blank=True)
    image_url = models.CharField(
        max_length=200, default="https://images2.imgbox.com/bd/3b/gdhTkjgA_o.jpg", blank=True)
    video_url = models.CharField(max_length=200, default="", blank=True)
    categorys = models.ManyToManyField(Category, blank=True)
    best_seller = models.BooleanField(default=False)
    start_price = models.FloatField(default=0)
    video_lenght = models.FloatField(default=0)
    price = models.FloatField(blank=True)
    teacher = models.ManyToManyField(
        User, blank=True, related_name='mycourses')
    teachers = models.ManyToManyField(
        User, blank=True, related_name='assist_in')
    # student = models.ManyToManyField(
    #     User, blank=True, related_name='allstudents')

    def __str__(self):
        c_creator = ','.join(str(v) for v in self.teacher.all())
        return f'{self.course_id}){self.course_title} By {c_creator}'


class Enroll(models.Model):
    types = (
        ('free', 'free'),
        ('visa', 'visa'),
        ('paypal', 'paypal'),)
    username = models.ManyToManyField(User, related_name='mylessons')
    course_id = models.ManyToManyField(Course, related_name='students')
    payment_type = models.CharField(max_length=50, choices=types)
    rate_scale = models.FloatField(max_length=5, blank=True, null=True)
    review = models.TextField(max_length=300, blank=True, null=True)
    complete_status = models.BooleanField(default=False, null=True)

    def __str__(self):
        course = ','.join(str(v) for v in self.course_id.all())
        users = ','.join(str(v) for v in self.username.all())
        # std = self.username.count
        return f'{course} Enroll By {users}'


class Lecture(models.Model):
    lecture_id = models.AutoField(primary_key=True)
    course_id = models.ManyToManyField(Course, related_name='lectures')
    # activity = models.ManyToManyField(User,   related_name='activity')
    lecture_title = models.CharField(max_length=100)
    video_url = models.CharField(max_length=200, default="", blank=True)
    image_url = models.CharField(max_length=200, default="", blank=True)
    slide_url = models.CharField(max_length=200, default="", blank=True)
    doc_url = models.CharField(max_length=200, default="", blank=True)

    def __str__(self):
        course = ','.join(str(v) for v in self.course_id.all())
        # lecture = ','.join(str(v) for v in self.lecture_id.all())
        # std = self.username.count
        return f'{self.lecture_id} ,{self.lecture_title} in {course}  '


class Lesson(models.Model):
    course_id = models.ManyToManyField(Course, related_name='lessons')
    lecture_id = models.ManyToManyField(Lecture, related_name='lesson')
    lesson_title = models.CharField(max_length=100)
    video_url = models.CharField(max_length=200, default="", blank=True)
    image_url = models.CharField(max_length=200, default="", blank=True)
    slide_url = models.CharField(max_length=200, default="", blank=True)
    doc_url = models.CharField(max_length=200, default="", blank=True)

    def __str__(self):
        course = ','.join(str(v) for v in self.course_id.all())
        lecture = ','.join(str(v) for v in self.lecture_id.all())
        # std = self.username.count
        return f'{self.id})({self.lesson_title}) in lecture ({lecture})'


class Lessonstatus(models.Model):
    course_id = models.ManyToManyField(Course, related_name='course')
    lecture_id = models.ManyToManyField(
        Lecture, blank=True, related_name='lecturestate')
    lesson_id = models.ManyToManyField(
        Lesson, blank=True, related_name='lessonstate')
    student = models.ManyToManyField(User, related_name='userstatus')
    status = models.BooleanField(default=False, null=True)

    def __str__(self):
        user = ','.join(str(v) for v in self.student.all())
        lecture = ','.join(str(v) for v in self.lecture_id.all())
        lesson = ','.join(str(v) for v in self.lesson_id.all())
        # std = self.username.count
        return f'({user} status in {lecture} in {lesson} is {self.status}))'


class Questions(models.Model):
    course_id = models.ManyToManyField(Course)
    lecture_id = models.ManyToManyField(
        Lecture, blank=True, related_name='asks')
    lesson_id = models.ManyToManyField(
        Lesson, blank=True, related_name='questions')
    question_num = models.IntegerField()
    question = models.CharField(max_length=300)
    option1 = models.CharField(max_length=200)
    option2 = models.CharField(max_length=200, blank=True, default='')
    option3 = models.CharField(max_length=200, blank=True, default='')
    option4 = models.CharField(max_length=200, blank=True, default='')
    answer = models.CharField(max_length=200, blank=True, default='')

    def __str__(self):
        course = ','.join(str(v) for v in self.course_id.all())
        lecture = ','.join(str(v) for v in self.lecture_id.all())
        lesson = ','.join(str(v) for v in self.lesson_id.all())
        # std = self.username.count
        # in lecture ({lecture})in course ({course})
        return f'{self.pk}({self.question_num}) in lesson({lesson}in lecture({lecture})'


class Discussion_board_for_lecture(models.Model):
    course_id = models.ManyToManyField(Course)
    lecture_id = models.ManyToManyField(Lecture, related_name='discuss')
    user_id = models.ManyToManyField(
        User, related_name='active')
    comment = models.TextField(max_length=300)
    create = models.DateTimeField(auto_now_add=True)


class Assignment(models.Model):
    course_id = models.ManyToManyField(Course)
    lecture_id = models.ManyToManyField(
        Lecture, related_name='lecture_assignment')
    title = models.TextField(max_length=100, default='Assignment')
    description = models.TextField(max_length=1000)
    image = models.URLField(max_length=250, blank=True)

    def __str__(self):
        course = ','.join(str(v) for v in self.course_id.all())
        # std = self.username.count
        return f'{self.id}){self.title})in ({course}) '


class Assignment_submission(models.Model):
    assignment_id = models.ManyToManyField(Assignment, related_name='answers')
    user_id = models.ManyToManyField(User, related_name='assigns')
    answer = models.CharField(max_length=1000)
    grade = models.IntegerField(blank=True, default=-1)
    create = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        user_id = ','.join(str(v) for v in self.user_id.all())
        assignment = ','.join(str(v) for v in self.assignment_id.all())
        # std = self.username.count
        return f'{self.id}){user_id})submit ({assignment}) '


class Assignment_status(models.Model):
    course_id = models.ManyToManyField(
        Course, related_name='course_assignments')
    lecture_id = models.ManyToManyField(
        Lecture, blank=True, related_name='lecture_status')
    assignment_id = models.ManyToManyField(
        Assignment, blank=True, related_name='assignment_status')
    student = models.ManyToManyField(User, related_name='complete')
    status = models.BooleanField(default=False, null=True)

    def __str__(self):
        user = ','.join(str(v) for v in self.student.all())
        lecture = ','.join(str(v) for v in self.lecture_id.all())
        # std = self.username.count
        return f'({user} status in {lecture} is {self.status}))'


class Final_project(models.Model):
    course_id = models.ManyToManyField(Course, related_name='final')
    title = models.CharField(max_length=100, default='Final')
    description = models.TextField(max_length=1000)
    video1_url = models.CharField(max_length=200, default="", blank=True)
    image1_url = models.CharField(max_length=200, default="", blank=True)
    video2_url = models.CharField(max_length=200, default="", blank=True)
    image2_url = models.CharField(max_length=200, default="", blank=True)

    def __str__(self):
        course = ','.join([str(v) for v in self.course_id.all()])
        return f'{self.title} in {course}'


class Final_submission(models.Model):
    final_id = models.ManyToManyField(Final_project, related_name='submission')
    user_id = models.ManyToManyField(User)
    answer = models.CharField(max_length=1000)
    grade = models.IntegerField(blank=True, default=-1)
    create = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        final = ','.join([str(v) for v in self.final_id.all()])
        user = ','.join([str(v) for v in self.user_id.all()])
        return f'{user} submit {final}'


class Grade(models.Model):
    course_id = models.ManyToManyField(Course, related_name='graduat')
    final_id = models.ManyToManyField(
        Final_submission, related_name='graduated')
    user_id = models.ManyToManyField(User, related_name='grade_student')
    cert = models.FileField(upload_to='course/cert/', null=True, blank=True)
    # total_grade = models.IntegerField(blank=True, default=-1)
    create = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        course = ','.join([str(v) for v in self.course_id.all()])
        user = ','.join([str(v) for v in self.user_id.all()])
        return f'{user} Grade in {course}'
