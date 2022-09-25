def managecourse(request, id):
    u_id = request.user.id
    user = User.objects.filter(
        Q(pk=u_id, type='Teacher') | Q(pk=u_id, type='Admin'))
    message = ''
    if not user:
        message = 'Only Teachers And Admins can Add Courses'
    if request.method == 'POST':
        form = addcourseForm(request.POST)
        if form.is_valid():
            largest = Course.objects.all().order_by('course_id').last()
            addCourse = form.save()
            addCourse.teacher.set(user)
            addCourse.save()
            return HttpResponseRedirect(reverse("course", args=((largest.course_id)+1,)))
    else:
        return render(request, "elearning/addcourse.html", {
            'form': addcourseForm(),
            'message': message,
        })


def managecourse(request, id):
    u_id = request.user.id
    user = User.objects.filter(
        Q(pk=u_id, type='Teacher') | Q(pk=u_id, type='Admin'))
    message = ''
    course = Course.objects.filter(
        course_id=id, teacher__id__in=user.all()).first()
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


def delcourse(request, id):
    course = Course.objects.filter(
        course_id=id, teacher__id__in=user.all()).first()
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
