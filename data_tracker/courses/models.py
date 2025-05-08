from django.db import models
from data_tracker.users.models import Mortals, Roles
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

# Status model to define the status for items
class Status(models.Model):
    title = models.CharField(max_length=100)
    video_related_status = models.BooleanField(default=False)
    platform_related_status = models.BooleanField(default=False, blank=True)
    youtube_related_status = models.BooleanField(default=False, blank=True)
    comments = models.TextField()
    
    class Meta:
        verbose_name = "Status"
        verbose_name_plural = "Statuses"

    def __str__(self):
        return self.title

# Course model to store course details and link to Items
class Course(models.Model):
    class CourseType(models.TextChoices):
        UKR_MATH = 'math(ukraine)', 'Math(Ukraine)'
        KA_MATH = 'math(khan academy)', 'Math(Khan Academy)'
        KA_SCIENCE = 'science(khan academy)', 'Science(Khan Academy)'
        UKR_SCIENCE = 'science(ukraine)', 'Science(Ukraine)'
        
    title = models.CharField(max_length=200)
    course_type = models.CharField(max_length=69, choices=CourseType.choices, default=CourseType.KA_MATH)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


# Item model to store item details and link to multiple courses
class Item(models.Model):
    class ItemType(models.TextChoices):
        ARTICLE = 'article', 'Article'
        EXERCISE = 'exercise', 'Exercise'

    title = models.CharField(max_length=512)
    link = models.URLField(max_length=512, unique=True)  # Store a URL as a link
    external_link = models.URLField(max_length=512, null=True, blank=True)  # Link to the item on the site
    courses = models.ManyToManyField(Course, related_name='items')  # Many-to-many relationship with Course
    type = models.CharField(max_length=10, choices=ItemType.choices)
    status = models.ForeignKey(Status, on_delete=models.SET_NULL, null=True)  # Foreign key to Status
    auditor = models.ForeignKey(Mortals, on_delete=models.SET_NULL, null=True, related_name='audited_items',blank=True)
    translator = models.ForeignKey(Mortals, on_delete=models.SET_NULL, null=True, related_name='translated_items',blank=True)
    number_of_words = models.IntegerField()  # Store number of words
    updated_by = models.ForeignKey(Mortals, on_delete=models.SET_NULL, null=True, blank=True)
    comments = models.TextField(blank=True)  # Store any comments
    last_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class Video(models.Model):
    title = models.CharField(max_length=200)
    portal_link = models.URLField(max_length=512,unique=True)
    localized_link = models.URLField(max_length=512,null=True, blank=True)
    yt_link = models.URLField(max_length=512,null=True, blank=True)
    translated_yt_link = models.URLField(max_length=512,null=True, blank=True)
    preview_link = models.URLField(max_length=512,null=True, blank=True)
    courses = models.ManyToManyField(Course, related_name='videos')
    video_status = models.ForeignKey(Status, on_delete=models.SET_NULL, null=True, blank=True, related_name='video_status')
    platform_status = models.ForeignKey(Status, on_delete=models.SET_NULL, null=True, blank=True, related_name='platform_status')
    youtube_status = models.ForeignKey(Status, on_delete=models.SET_NULL, null=True, blank=True, related_name='youtube_status')
    translation_issue = models.BooleanField(default=False)
    auditor = models.ForeignKey(Mortals, on_delete=models.SET_NULL, null=True, related_name='audited_videos',blank=True)
    actor = models.ForeignKey(Mortals, on_delete=models.SET_NULL, null=True, related_name='translated_videos',blank=True)
    duration = models.DurationField(null=True,blank=True)
    updated_by = models.ForeignKey(Mortals, on_delete=models.SET_NULL, null=True, blank=True)
    comments = models.TextField(null=True, blank=True)
    type = models.CharField(max_length=10,blank=True, null=True, default="Video")
    last_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


# ActionLog model to track changes (create, update, delete) for items and courses
class ActionLog(models.Model):
    ACTION_CHOICES = [
        ('create', 'Created'),
        ('update', 'Updated'),
    ]

    action = models.CharField(choices=ACTION_CHOICES, max_length=10)
    type = models.CharField(max_length=50)
    item = models.ForeignKey(Item, on_delete=models.SET_NULL, null=True, blank=True)
    video = models.ForeignKey(Video, on_delete=models.SET_NULL, null=True, blank=True)
    who = models.ForeignKey(Mortals, on_delete=models.SET_NULL, null=True, blank=True)  # Track who performed the action
    new_status = models.ForeignKey('Status', on_delete=models.SET_NULL, null=True, blank=True)  # Adjust based on your model
    date = models.DateTimeField(auto_now=True)
    comment = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.action} {self.type} by {self.who.first_name} {self.who.last_name} at {self.date}"
    
class BugType(models.Model):
    name = models.CharField(max_length=255)    
    description = models.TextField(null=True, blank=True)
    
    class Meta:
        verbose_name = ("Bug type")
        verbose_name_plural = ("Bug types")

    def __str__(self):
        return self.name

    
class BugReport(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, related_name='bug_content_type')
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    
    reported_by_content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True, blank=True, related_name='bug_reported_by_type')
    reported_by_object_id = models.PositiveIntegerField(null=True, blank=True)
    reported_by = GenericForeignKey('reported_by_content_type', 'reported_by_object_id')

    title = models.CharField(max_length=255)
    bug_type = models.ForeignKey(BugType, on_delete=models.CASCADE)
    description = models.TextField()
    assigned_to = models.ForeignKey(Mortals, on_delete=models.SET_NULL, null=True, blank=True, related_name="assigned_to")
    created_at = models.DateTimeField(auto_now=True)
    is_resolved = models.BooleanField(default=False)
    added_by = models.ForeignKey(Mortals, on_delete=models.SET_NULL, null=True, blank=True, related_name="added_by")

    class Meta:
        indexes = [
            models.Index(fields=['content_type', 'object_id']),
        ]
        verbose_name = ("Bug")
        verbose_name_plural = ("Bugs")

    def __str__(self):
        return f"{self.title} ({self.content_type} #{self.object_id})"
