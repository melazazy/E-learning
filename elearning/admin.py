from django.contrib import admin

from .models import *

# Register your models here.

admin.site.register(User)
admin.site.register(Category)
admin.site.register(Course)
admin.site.register(Lecture)
admin.site.register(Assignment)
admin.site.register(Assignment_submission)
admin.site.register(Assignment_status)
admin.site.register(Lesson)
admin.site.register(Lessonstatus)
admin.site.register(Questions)
admin.site.register(Enroll)
admin.site.register(Discussion_board_for_lecture)
admin.site.register(Final_project)
admin.site.register(Final_submission)
admin.site.register(Grade)
