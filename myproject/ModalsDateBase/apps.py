from django.apps import AppConfig


class ModalsdatebaseConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ModalsDateBase'
    
    def ready(self) -> None:
        from . import signals
