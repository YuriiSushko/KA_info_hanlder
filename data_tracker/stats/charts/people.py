from django.db.models import Count
from data_tracker.courses.models import ActionLog
from data_tracker.stats.charts.base import ChartViewBase
from data_tracker.stats.forms import PersonFilterForm
from django.db.models.functions import ExtractMonth
import calendar

class PeopleChart(ChartViewBase):
    title = "People stats"
    form_class = PersonFilterForm        
        
    def get_chart_data(self, filters):
        qs = ActionLog.objects.all()

        selected_person = filters.get('person')
        if selected_person:
            qs = qs.filter(who=selected_person)

        selected_month = filters.get('month')
        if selected_month:
            qs = qs.filter(date__month=int(selected_month))
        
        if not selected_person and not selected_month:
            return [], []

        qs = qs.annotate(month_num=ExtractMonth('date'))
        results = qs.values('action', 'month_num').annotate(count=Count('id')).order_by('month_num', 'action')

        month_numbers = range(1, 13)
        month_labels = [calendar.month_name[m] for m in month_numbers]

        action_types = [choice[0] for choice in ActionLog.ACTION_CHOICES]
        data_by_action = {action: [0]*12 for action in action_types}

        for row in results:
            action = row['action']
            month_index = row['month_num'] - 1
            count = row['count']
            if action in data_by_action and 0 <= month_index < 12:
                data_by_action[action][month_index] = count

        series = [
            {"label": action, "data": data_by_action[action]}
            for action in action_types
        ]

        return month_labels, series

    