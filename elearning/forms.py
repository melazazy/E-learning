from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.urls import reverse_lazy
# from django.core.urlresolvers import reverse
# from django.forms import ModelForm
from .models import *


class userForm(forms.ModelForm):
    class Meta:
        model = User
        # fields = "__all__"
        fields = ['first_name', 'last_name', 'image']


class enrollForm(forms.Form):
    class Meta:
        model = Enroll
        # payment_type = forms.CharField(max_length=50)
        type = forms.CharField(label='Your name')


class addcourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['course_title', 'describe', 'image_url',
                  'video_url', 'categorys', 'start_price', 'video_lenght', 'price']


class addlectureForm(forms.ModelForm):
    class Meta:
        model = Lecture
        fields = ['lecture_title', 'image_url',
                  'video_url', 'slide_url', 'doc_url']


class addlessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ['lesson_title', 'image_url',
                  'video_url', 'slide_url', 'doc_url']


class addquestionForm(forms.ModelForm):
    class Meta:
        model = Questions
        fields = ['question_num', 'question', 'option1',
                  'option2', 'option3', 'option4', 'answer']


class addassignmentForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = ['title', 'description', 'image']


class addfinalForm(forms.ModelForm):
    class Meta:
        model = Final_project
        fields = ['title', 'description', 'video1_url',
                  'image1_url', 'video2_url', 'image2_url']


class gradeForm(forms.ModelForm):
    class Meta:
        model = Grade
        fields = ['cert']


# class UserChangeForm(forms.ModelForm):
#     """A form for updating users. Includes all the fields on
#     the user, but replaces the password field with admin's
#     password hash display field.
#     """
#     password = ReadOnlyPasswordHashField(label=("Password"),
#                                          help_text=("Raw passwords are not stored, so there is no way to see "
#                                                     "this user's password, but you can change the password "
#                                                     "using <a href=\"../password/\">this form</a>."))

#     class Meta:
#         model = User
#         fields = ['username', 'password']

    # def clean_password(self):
    #     # Regardless of what the user provides, return the initial value.
    #     # This is done here, rather than on the field, because the
    #     # field does not have access to the initial value
    #     return self.initial["password"]

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['password'].help_text = (
    #         "Raw passwords are not stored, so there is no way to see "
    #         "this user's password, but you can <a href=\"%s\"> "
    #         "<strong>Change the Password</strong> using this form</a>."
    #     ) % reverse_lazy('admin:auth_user_password_change', args=[self.instance.id])
