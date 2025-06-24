from django.contrib import admin
from django.urls import path
from django.template.response import TemplateResponse
from django.utils.timezone import now
from datetime import timedelta
from django.db.models.functions import TruncDate
from django.db.models import Count

from data_tracker.users.models import Mortals
from data_tracker.stats.models import ChartViewEntry
from data_tracker.admin_site import custom_admin_site

from django.shortcuts import redirect

class ChartAdmin(admin.ModelAdmin):
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path("charts/", self.admin_site.admin_view(self.charts_view), name="custom_charts"),
        ]
        return custom_urls + urls

    def changelist_view(self, request, extra_context=None):
        # Redirect the default view to our charts
        return redirect("admin:custom_charts")

    def charts_view(self, request):
        from data_tracker.users.models import Mortals
        from django.utils.timezone import now
        from datetime import timedelta
        from django.db.models.functions import TruncDate
        from django.db.models import Count
        from django.template.response import TemplateResponse

        week_ago = now() - timedelta(days=7)
        registrations = (
            Mortals.objects.filter(last_seen__gte=week_ago)
            .annotate(date=TruncDate('last_seen'))
            .values('date')
            .annotate(count=Count('id'))
            .order_by('date')
        )

        labels = [r['date'].strftime("%Y-%m-%d") for r in registrations]
        values = [r['count'] for r in registrations]

        context = dict(
            self.admin_site.each_context(request),
            chart_labels=labels,
            chart_values=values,
            title="📊 User Registration Chart",
        )

        return TemplateResponse(request, "admin/custom_charts.html", context)

custom_admin_site.register(ChartViewEntry, ChartAdmin)