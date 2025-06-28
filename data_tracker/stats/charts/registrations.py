from datetime import timedelta
from django.utils.timezone import now
from django.db.models.functions import TruncDate
from django.db.models import Count
from data_tracker.users.models import Mortals
from data_tracker.stats.charts.base import ChartViewBase
from data_tracker.stats.forms import RegistrationChartFilterForm

class RegistrationChart(ChartViewBase):
    title = "User Registrations"
    form_class = RegistrationChartFilterForm

    def get_chart_data(self, filters):
        days = filters.get("days", 7)
        start_date = now() - timedelta(days=days)

        qs = (
            Mortals.objects.filter(last_seen__gte=start_date)
            .annotate(date=TruncDate('last_seen'))
            .values('date')
            .annotate(count=Count('id'))
            .order_by('date')
        )

        labels = [entry["date"].strftime("%Y-%m-%d") for entry in qs]
        values = [entry["count"] for entry in qs]
        return labels, values
