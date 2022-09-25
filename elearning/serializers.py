from rest_framework import serializers
from .models import *


class userSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'image']


class enrollSerializer(serializers.ModelSerializer):
    student = userSerializer(read_only=True, many=True)

    class Meta:
        model = Enroll
        fields = '__all__'


class courseSerializer(serializers.ModelSerializer):
    teacher = userSerializer(read_only=True, many=True)
    teachers = userSerializer(read_only=True, many=True)
    students = enrollSerializer(read_only=True, many=True)

    class Meta:
        model = Course
        fields = '__all__'


class lessonSerializer(serializers.ModelSerializer):
    course_id = courseSerializer(read_only=True, many=True)

    class Meta:
        model = Lesson
        fields = '__all__'


class QSerializer(serializers.ModelSerializer):
    course_id = courseSerializer(read_only=True, many=True)
    lesson = lessonSerializer(read_only=True, many=True)

    class Meta:
        model = Questions
        fields = '__all__'


class discussionSerializer(serializers.ModelSerializer):
    user_id = userSerializer(read_only=True, many=True)

    class Meta:
        model = Discussion_board_for_lecture
        fields = '__all__'


class LessonstatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lessonstatus
        fields = '__all__'


class lectureSerializer(serializers.ModelSerializer):
    course_id = courseSerializer(read_only=True, many=True)
    lesson = lessonSerializer(read_only=True, many=True)
    discuss = discussionSerializer(read_only=True, many=True)
    asks = QSerializer(read_only=True, many=True)
    lecturestate = LessonstatusSerializer(read_only=True, many=True)

    class Meta:
        model = Lecture
        fields = '__all__'


class lessonsSerializer(serializers.ModelSerializer):
    course_id = courseSerializer(read_only=True, many=True)
    lecture_id = lectureSerializer(read_only=True, many=True)
    questions = QSerializer(read_only=True, many=True)
    lessonstate = LessonstatusSerializer(read_only=True, many=True)

    class Meta:
        model = Lesson
        fields = '__all__'


class assignmentSubmissionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Assignment_submission
        fields = '__all__'


class assignmentStatusSerializer(serializers.ModelSerializer):

    class Meta:
        model = Assignment_status
        fields = '__all__'


class assignmentSerializer(serializers.ModelSerializer):
    answers = assignmentSubmissionSerializer(read_only=True, many=True)
    assignment_status = assignmentStatusSerializer(read_only=True, many=True)

    class Meta:
        model = Assignment
        fields = '__all__'


class FinalSubmissionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Final_submission
        fields = '__all__'


class Final_projectSerializer(serializers.ModelSerializer):
    submission = FinalSubmissionSerializer(read_only=True, many=True)

    class Meta:
        model = Final_project
        fields = '__all__'
