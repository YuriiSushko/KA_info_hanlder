from django.apps import AppConfig

class CoursesConfig(AppConfig):
    name = 'data_tracker.courses'  # The name of your app

    def ready(self):
        import data_tracker.courses.signals  # Register the signals
        print("Signals have been registered!")
