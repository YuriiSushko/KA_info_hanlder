from django.shortcuts import render, get_object_or_404, redirect
from data_tracker.courses.models import Course, ActionLog, Item, People, Role
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.utils.timezone import now

# # View to create a new course
# def create_course(request):
#     if request.method == 'POST':  # Check if the form is submitted via POST
#         title = request.POST.get('title')  # Get the course title from the form
#         description = request.POST.get('description')  # Get the description

#         # Create the new Course object
#         course = Course.objects.create(title=title, description=description)

#         # Create an ActionLog entry for course creation
#         ActionLog.objects.create(
#             action='create',
#             object_type='Course',
#             object_id=course.id,
#             people=request.user,  # Automatically get the user who created the course
#             new_status=None,  # No status for course (if applicable)
#             date=now(),  # Automatically set the timestamp
#             comment=f"Course created: {course.title}"  # Custom comment for the action
#         )

#         return redirect('course_list')  # Redirect to a list view of courses (or wherever you need)
    
#     return render(request, 'courses/create_course.html')  # Render the form if it's a GET request

# # View to delete a course
# def delete_course(request, course_id):
#     course = get_object_or_404(Course, id=course_id)  # Get the course to delete

#     if request.method == 'POST':  # If the form is submitted via POST
#         course.delete()  # Delete the course

#         return redirect('course_list')  # Redirect to a list view of courses (or wherever you need)

#     return render(request, 'courses/delete_course.html', {'course': course})  # Render the delete confirmation form

# def action_log_list(request):
#     action_logs = ActionLog.objects.all().order_by('-date')

#     # Filter by action type if provided
#     action_filter = request.GET.get('action')
#     if action_filter:
#         action_logs = action_logs.filter(action=action_filter)

#     # Filter by username if provided
#     user_filter = request.GET.get('user')
#     if user_filter:
#         action_logs = action_logs.filter(people__username__icontains=user_filter)

#     return render(request, 'courses/action_log_list.html', {'action_logs': action_logs})


# def people_list(request):
#     people = People.objects.all()
#     return render(request, 'courses/people_list.html', {'people': people})

# def role_list(request):
#     roles = Role.objects.all()
#     return render(request, 'courses/role_list.html', {'roles': roles})
