from django.urls import path
from data_tracker.courses import views

urlpatterns = [
    path('create/', views.create_course, name='create_course'),
    path('update/<int:course_id>/', views.update_course, name='update_course'),
    path('delete/<int:course_id>/', views.delete_course, name='delete_course'),
]
