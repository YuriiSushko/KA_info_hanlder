from django.db import models
from data_tracker.users.models import Mortals, Roles

# Status model to define the status for items
class Status(models.Model):
    title = models.CharField(max_length=100)
    comments = models.TextField()
    
    class Meta:
        verbose_name = "Status"
        verbose_name_plural = "Statuses"

    def __str__(self):
        return self.title


# # Role model to define roles for people
# class Role(models.Model):
#     title = models.CharField(max_length=100)

#     def __str__(self):
#         return self.title


# # People model to store people's details and their roles
# class People(models.Model):
#     name = models.CharField(max_length=200)
#     surname = models.CharField(max_length=100)
#     roles = models.ManyToManyField(Role)  # Many-to-many relationship with Role

#     def __str__(self):
#         return f"{self.name} {self.surname}"


# Course model to store course details and link to Items
class Course(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


# Item model to store item details and link to multiple courses
class Item(models.Model):
    class ItemType(models.TextChoices):
        ARTICLE = 'article', 'Article'
        EXERCISE = 'exercise', 'Exercise'

    title = models.CharField(max_length=200)
    link = models.URLField(unique=True)  # Store a URL as a link
    external_link = models.URLField(null=True, blank=True)  # Link to the item on the site
    courses = models.ManyToManyField(Course, related_name='items')  # Many-to-many relationship with Course
    type = models.CharField(max_length=10, choices=ItemType.choices)
    status = models.ForeignKey(Status, on_delete=models.SET_NULL, null=True)  # Foreign key to Status
    auditor = models.ForeignKey(Mortals, on_delete=models.SET_NULL, null=True, related_name='audited_items',blank=True)
    translator = models.ForeignKey(Mortals, on_delete=models.SET_NULL, null=True, related_name='translated_items',blank=True)
    number_of_words = models.IntegerField()  # Store number of words
    updated_by = models.ForeignKey(Mortals, on_delete=models.SET_NULL, null=True, blank=True)
    comments = models.TextField(blank=True)  # Store any comments
    last_modified = models.DateTimeField(auto_now=True)  # Timestamp for last modification

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
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    who = models.ForeignKey(Mortals, on_delete=models.CASCADE, null=True, blank=True)  # Track who performed the action
    new_status = models.ForeignKey('Status', on_delete=models.SET_NULL, null=True, blank=True)  # Adjust based on your model
    date = models.DateTimeField(auto_now_add=True)
    comment = models.TextField()

    def __str__(self):
        return f"{self.action} {self.type} by {self.who.first_name} {self.who.last_name} at {self.date}"
    
