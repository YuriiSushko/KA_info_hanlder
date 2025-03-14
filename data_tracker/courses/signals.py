from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.utils.timezone import now
from data_tracker.courses.models import Course, Item, ActionLog, People

# Signal handler for creating ActionLog when a Course is created or updated
@receiver(post_save, sender=Course)
def log_course_action(sender, instance, created, **kwargs):
    action = 'create' if created else 'update'
    
    # Example: Fetch the current user (replace with actual logic for your setup)
    people = None  # Replace with actual logic to get the current user

    ActionLog.objects.create(
        action=action,
        object_type='Course',
        object_id=instance.id,
        people=people,
        date=now()
    )


# Signal handler for creating ActionLog when an Item is created or updated
@receiver(post_save, sender=Item)
def log_item_action(sender, instance, created, **kwargs):
    action = 'create' if created else 'update'
    
    # Example: Fetch the current user (replace with actual logic for your setup)
    people = None  # Replace with actual logic

    ActionLog.objects.create(
        action=action,
        object_type='Item',
        object_id=instance.id,
        people=people,
        date=now()
    )


# Signal handler for creating ActionLog when a Course is deleted
@receiver(post_delete, sender=Course)
def log_course_delete(sender, instance, **kwargs):
    people = None  # Replace with actual logic to get the current user

    ActionLog.objects.create(
        action='delete',
        object_type='Course',
        object_id=instance.id,
        people=people,
        date=now()
    )


# Signal handler for creating ActionLog when an Item is deleted
@receiver(post_delete, sender=Item)
def log_item_delete(sender, instance, **kwargs):
    people = None  # Replace with actual logic to get the current user

    ActionLog.objects.create(
        action='delete',
        object_type='Item',
        object_id=instance.id,
        people=people,
        date=now()
    )
