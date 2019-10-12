from django.apps import AppConfig


class StayunderflowWebappConfig(AppConfig):
    name = 'StayUnderflow_WebApp'

    def ready(self):
        import StayUnderflow_WebApp.signals
