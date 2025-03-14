# courses/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from data_tracker.courses.models import Course
from data_tracker.courses.signals import log_course_action, log_course_delete  # Import your signal handlers

# View to create a new course
def create_course(request):
    if request.method == 'POST':  # Check if the form is submitted via POST
        title = request.POST.get('title')  # Get the course title from the form
        description = request.POST.get('description')  # Get the description

        # Create the new Course object
        course = Course.objects.create(title=title, description=description)

        # Log the action with the current user
        log_course_action(sender=Course, instance=course, created=True, user=request.user)

        return redirect('course_list')  # Redirect to a list view of courses (or wherever you need)
    
    return render(request, 'courses/create_course.html')  # Render the form if it's a GET request


# View to update an existing course
def update_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)  # Get the course to update

    if request.method == 'POST':  # If the form is submitted via POST
        course.title = request.POST.get('title', course.title)  # Update the title
        course.description = request.POST.get('description', course.description)  # Update the description
        course.save()  # Save the updated course

        # Log the action with the current user
        log_course_action(sender=Course, instance=course, created=False, user=request.user)

        return redirect('course_list')  # Redirect to a list view of courses (or wherever you need)

    return render(request, 'courses/update_course.html', {'course': course})  # Render the form if it's a GET request


# View to delete a course
def delete_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)  # Get the course to delete

    if request.method == 'POST':  # If the form is submitted via POST
        course.delete()  # Delete the course

        # Log the deletion action with the current user
        log_course_delete(sender=Course, instance=course, user=request.user)

        return redirect('course_list')  # Redirect to a list view of courses (or wherever you need)

    return render(request, 'courses/delete_course.html', {'course': course})  # Render the delete confirmation form
