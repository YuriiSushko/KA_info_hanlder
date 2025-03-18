from django.db import models


# Status model to define the status for items
class Status(models.Model):
    title = models.CharField(max_length=100)
    comments = models.TextField()

    def __str__(self):
        return self.title


# Role model to define roles for people
class Role(models.Model):
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title


# People model to store people's details and their roles
class People(models.Model):
    name = models.CharField(max_length=200)
    surname = models.CharField(max_length=100)
    roles = models.ManyToManyField(Role)  # Many-to-many relationship with Role

    def __str__(self):
        return self.name


# Course model to store course details and link to Items
class Course(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


# Item model to store item details and link to multiple courses
class Item(models.Model):
    ITEM_TYPE_CHOICES = [
        ('article', 'Article'),
        ('exercise', 'Exercise'),
    ]

    title = models.CharField(max_length=200)
    link = models.URLField()  # Store a URL as a link
    courses = models.ManyToManyField(Course, related_name='items')  # Many-to-many relationship with Course
    type = models.CharField(max_length=10, choices=ITEM_TYPE_CHOICES)  # Article or Exercise
    status = models.ForeignKey(Status, on_delete=models.SET_NULL, null=True)  # Foreign key to Status
    auditor = models.ForeignKey(People, on_delete=models.SET_NULL, null=True, related_name='audited_items')  # Foreign key to People (Auditor)
    translator = models.ForeignKey(People, on_delete=models.SET_NULL, null=True, related_name='translated_items')  # Foreign key to People (Translator)
    number_of_words = models.IntegerField()  # Store number of words
    comments = models.TextField()  # Store any comments

    def __str__(self):
        return self.title


# ActionLog model to track changes (create, update, delete) for items and courses
class ActionLog(models.Model):
    ACTION_CHOICES = [
        ('create', 'Created'),
        ('update', 'Updated'),
        ('delete', 'Deleted'),
    ]

    action = models.CharField(choices=ACTION_CHOICES, max_length=10)
    object_type = models.CharField(max_length=50)
    object_id = models.PositiveIntegerField()
    people = models.ForeignKey(People, on_delete=models.CASCADE)  # Foreign key to the People model
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.action} {self.object_type} by {self.people.name} at {self.date}"
