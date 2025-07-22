import json
from django.db.models import Count
from data_tracker.courses.models import Item, Video, Status
from data_tracker.stats.charts.base import ChartViewBase
from data_tracker.stats.forms import CourseFilterForm
from django.db.models import Q
from collections import defaultdict

class CourseChart(ChartViewBase):
    title = "Content in Courses by Status"
    form_class = CourseFilterForm

    def get_chart_data(self, filters):
        selected_course = filters.get("course")
        if not selected_course:
            return [], [], {}

        status_title_map = defaultdict(list)
        for status in Status.objects.all():
            status_title_map[status.title].append(status.id)

        status_flags = {
            status.id: status.video_related_status
            for status in Status.objects.all()
        }
        
        #======================================
        title_flags = defaultdict(set)

        for status in Status.objects.all():
            title_flags[status.title].add(status.video_related_status)

        title_type_map = {}
        for title, flags in title_flags.items():
            if flags == {True}:
                title_type_map[title] = "video"
            elif flags == {False}:
                title_type_map[title] = "item"
            else:
                title_type_map[title] = "both"
                
        #=========================================
        def count_items(item_type):
            return dict(
                Item.objects.filter(courses=selected_course, type=item_type)
                .values_list("status__id")
                .annotate(count=Count("id"))
            )
            
        def get_video_counts_by_status_ids(status_ids):
            return Video.objects.filter(
                courses=selected_course
            ).filter(
                Q(video_status__id__in=status_ids) |
                Q(platform_status__id__in=status_ids) |
                Q(youtube_status__id__in=status_ids)
            ).values("id").distinct().count()

        item_counts = {
            "exercise": count_items("exercise"),
            "article": count_items("article"),
        }
        
        status_rows = []
        for title, ids in status_title_map.items():
            ex_total = sum(item_counts["exercise"].get(i, 0) for i in ids)
            ar_total = sum(item_counts["article"].get(i, 0) for i in ids)
            vid_total = get_video_counts_by_status_ids(ids)

            has_video_status = any(status_flags.get(i, False) for i in ids)
            has_item_status = any(not status_flags.get(i, False) for i in ids)

            if has_video_status and not has_item_status:
                ex_total = None
                ar_total = None
            elif has_item_status and not has_video_status:
                vid_total = None

            status_rows.append((title, ex_total, ar_total, vid_total))

        def append_special(title, ex_val, ar_val, vid_val):
            status_rows.append((title, ex_val, ar_val, vid_val))

        ti_count = Video.objects.filter(courses=selected_course, translation_issue=True).count()
        if ti_count > 0:
            append_special("Translation Issue (video)", 0, 0, ti_count)

        np_vid = Video.objects.filter(
            Q(video_status__isnull=True),platform_status__isnull=True,youtube_status__isnull=True,courses=selected_course,
            ).count()
        np_ar = Item.objects.filter(
            courses=selected_course, type="article"
        ).filter( Q(status__isnull=True)).count()
        np_ex = Item.objects.filter(
            courses=selected_course, type="exercise"
        ).filter(Q(status__isnull=True)).count()

        if any([np_vid, np_ar, np_ex]):
            append_special("Without status", np_ex, np_ar, np_vid)

        def usage_priority(entry):
            title, _, _, _ = entry
            status_type = title_type_map.get(title, "item")
            if status_type == "both":
                group = 0
            elif status_type == "item":
                group = 1
            elif status_type == "video":
                group = 2
            else:
                group = 3
            return (group, title.lower())   
        status_rows.sort(key=usage_priority)

        # Unpack
        status_titles = []
        exercise_values, article_values, video_values = [], [], []
        for title, ex, ar, vid in status_rows:
            status_titles.append(title)
            exercise_values.append(ex)
            article_values.append(ar)
            video_values.append(vid)
        
        datasets = []
        if any(v is not None for v in exercise_values):
            datasets.append({"label": "Exercise", "data": exercise_values, "stack": "exercise", "skipNull": "true", "maxBarThickness": "30"})
        if any(v is not None for v in article_values):
            datasets.append({"label": "Article", "data": article_values, "stack": "article",  "skipNull": "true", "maxBarThickness": "30"})
        if any(v is not None for v in video_values):
            datasets.append({"label": "Video", "data": video_values, "stack": "video", "skipNull": "true", "maxBarThickness": "30"})

        video_total_ids = Video.objects.filter(courses=selected_course).values_list("id", flat=True).distinct()
        
        extra = {
            "totals": {
                "Exercise": sum(v for v in exercise_values if v is not None),
                "Article": sum(v for v in article_values if v is not None),
                "Video": video_total_ids.count(),
            }
        }
        
        return json.dumps(status_titles), json.dumps(datasets), extra
    
class GeneralProgressByCourse(ChartViewBase):
    title = "Validated/Processed/Not Processed"
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
        processed_ex = qs_exercises.exclude(Q(status__title="Translated") | Q(status__isnull=True)).count()
        not_processed_ex = qs_exercises.filter(Q(status__title="Translated") | Q(status__isnull=True)).count()

        # Articles
        total_ar = qs_articles.count()
        validated_ar = qs_articles.filter(status__title="Validated").count()
        processed_ar = qs_articles.exclude(Q(status__title="Translated") | Q(status__isnull=True)).count()
        not_processed_ar = qs_articles.filter(Q(status__title="Translated") | Q(status__isnull=True)).count()

        # Videos
        total_vid = qs_videos.count()
        validated_vid = qs_videos.filter(video_status__title="Validated").count()
        processed_vid = qs_videos.exclude(
            Q(video_status__isnull=True) | Q(video_status__title="Recorded"), platform_status__isnull=True,youtube_status__isnull=True
        ).count()
        not_processed_vid = qs_videos.filter(
            Q(video_status__isnull=True) | Q(video_status__title="Recorded"), platform_status__isnull=True, youtube_status__isnull=True
        ).count()
        
        exercise_data = [total_ex, validated_ex, processed_ex, not_processed_ex]
        article_data = [total_ar, validated_ar, processed_ar, not_processed_ar]
        video_data = [total_vid, validated_vid, processed_vid, not_processed_vid]

        datasets = [
            {"label": "Exercises", "data": exercise_data},
            {"label": "Articles", "data": article_data},
            {"label": "Videos", "data": video_data},
        ]

        return (
            json.dumps(labels),
            json.dumps(datasets)
        )
