from django.db.models import Count
from data_tracker.courses.models import Item, Video, Status
from data_tracker.stats.charts.base import ChartViewBase
from data_tracker.stats.forms import CourseFilterForm

class CourseChart(ChartViewBase):
    title = "Content in Courses by Status"
    form_class = CourseFilterForm

    def get_chart_data(self, filters):
        selected_course = filters.get('course')
        if not selected_course:
            return [], []
        
        all_statuses = list(Status.objects.all())
        status_ids = [status.id for status in all_statuses]
        status_titles = [status.title for status in all_statuses]

        def count_items_by_type(item_type):
            """Returns dict of {status_id: count} for Items of given type."""
            return dict(
                Item.objects.filter(courses=selected_course, type=item_type)
                    .values_list('status__id')
                    .annotate(count=Count('id'))
            )

        def count_videos_by_status_field(field_name):
            """Returns dict of {status_id: count} for a Video status field."""
            return dict(
                Video.objects.filter(courses=selected_course)
                    .values_list(f"{field_name}__id")
                    .annotate(count=Count('id'))
            )

        exercise_counts = count_items_by_type("exercise")
        article_counts = count_items_by_type("article")

        video_status_fields = ["video_status", "platform_status", "youtube_status"]
        video_counts_by_field = [
            count_videos_by_status_field(field) for field in video_status_fields
        ]

        exercise_values = [exercise_counts.get(sid, 0) for sid in status_ids]
        article_values = [article_counts.get(sid, 0) for sid in status_ids]

        video_values = []
        for i, sid in enumerate(status_ids):
            total = sum(vc.get(sid, 0) for vc in video_counts_by_field)
            video_values.append(total)
                
        datasets = [
            {"label": "Exercise", "data": exercise_values},
            {"label": "Article", "data": article_values},
            {"label": "Video", "data": video_values},
        ]

        translation_issue_count = Video.objects.filter(
            courses=selected_course,
            translation_issue=True
        ).count()

        if translation_issue_count > 0:
            status_titles.append("Translation Issue")
            for dataset in datasets:
                dataset["data"].append(0)
            datasets.append({
                "label": "Video",
                "data": [0] * (len(status_titles) - 1) + [translation_issue_count]
            })
            
        extra = {
                    "totals": {
                        "Exercise": sum(exercise_values),
                        "Article": sum(article_values),
                        "Video": sum(video_values),
                    }
                }

        return status_titles, datasets, extra
    
class GeneralProgressByCourse(ChartViewBase):
    title = "Processed counts in Course by Status"
    form_class = CourseFilterForm

    def get_chart_data(self, filters):
        selected_course = filters.get('course')
        if not selected_course:
            return [], []

        qs_exercises = Item.objects.filter(courses=selected_course, type="exercise")
        qs_articles = Item.objects.filter(courses=selected_course, type="article")
        qs_videos = Video.objects.filter(courses=selected_course)

        labels = ["Total", "Validated", "Processed", "Not processed"]

        # Exercises
        total_ex = qs_exercises.count()
        validated_ex = qs_exercises.filter(status__title="Validated").count()
        processed_ex = qs_exercises.exclude(status__title__in=["Translated", None]).count()
        not_processed_ex = qs_exercises.filter(status__title__in=["Translated", None]).count()

        # Articles
        total_ar = qs_articles.count()
        validated_ar = qs_articles.filter(status__title="Validated").count()
        processed_ar = qs_articles.exclude(status__title__in=["Translated", None]).count()
        not_processed_ar = qs_articles.filter(status__title__in=["Translated", None]).count()

        # Videos
        total_vid = qs_videos.count()
        validated_vid = qs_videos.filter(video_status__title="Validated").count()
        processed_vid = qs_videos.exclude(video_status__title__in=["Recorded", None]).count()
        not_processed_vid = qs_videos.filter(video_status__title__in=["Recorded", None]).count()

        exercise_data = [total_ex, validated_ex, processed_ex, not_processed_ex]
        article_data = [total_ar, validated_ar, processed_ar, not_processed_ar]
        video_data = [total_vid, validated_vid, processed_vid, not_processed_vid]

        datasets = [
            {"label": "Exercises", "data": exercise_data},
            {"label": "Articles", "data": article_data},
            {"label": "Videos", "data": video_data},
        ]

        return labels, datasets
