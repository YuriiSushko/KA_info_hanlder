from django.db import models

class ChartViewEntry(models.Model):
    class Meta:
        verbose_name_plural = "Charts"
        permissions = []

    def __str__(self):
        return "Open Charts"
