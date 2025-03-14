from django.apps import AppConfig

class CoursesConfig(AppConfig):
    name = 'courses'

    def ready(self):
        import courses.signals  # Import the signals to register them
