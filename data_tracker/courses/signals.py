from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.timezone import now
from data_tracker.courses.models import Item, ActionLog
from data_tracker.users.models import Mortals

@receiver(post_save, sender=Item)
def log_item_action(sender, instance, created, **kwargs):
    # Skip creating an ActionLog entry if this is a new item (created)
    action='update'
    if created:
        action = 'create'

    # If the item is updated, track the user who made the change
    updated_by_user = instance.updated_by  # The user who made the update (set in admin)

    # Prepare a comment for the action
    comment = f"Item updated: {instance.title}"

    # Log the update action in the ActionLog
    ActionLog.objects.create(
        action=action,  # Action type is 'update'
        type=instance.type,  # The type of object being updated
        item=instance,  # The ID of the updated item
        who=updated_by_user,  # The user who performed the update
        new_status=instance.status,  # The new status of the item
        date=now(),  # Timestamp of the update
        comment=comment  # A custom comment describing the update
    )