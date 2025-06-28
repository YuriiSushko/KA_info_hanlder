from django.urls import path
from django.shortcuts import redirect
from django.template.response import TemplateResponse
from django.contrib import admin
from data_tracker.stats.models import ChartViewEntry
from data_tracker.stats.charts.registrations import RegistrationChart
from data_tracker.stats.charts.courses import CourseChart, GeneralProgressByCourse
from data_tracker.admin_site import custom_admin_site

class ChartAdmin(admin.ModelAdmin):
    chart_view_classes = [CourseChart, GeneralProgressByCourse]
    
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path("charts/", self.admin_site.admin_view(self.chart_view), name="custom_charts"),
        ]
        return custom_urls + urls

    def changelist_view(self, request, extra_context=None):
        return redirect("admin:custom_charts")

    def chart_view(self, request):
        charts_context = []
        for chart_cls in self.chart_view_classes:
            chart = chart_cls()
            chart_context = chart.get_context_data(request)
            charts_context.append(chart_context)

        context = dict(
            self.admin_site.each_context(request),
            charts=charts_context,
            title="Chart Dashboard",
        )
        return TemplateResponse(request, "admin/custom_charts.html", context)

custom_admin_site.register(ChartViewEntry, ChartAdmin)