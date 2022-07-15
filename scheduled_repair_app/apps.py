from django.apps import AppConfig


class ScheduledRepairAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'scheduled_repair_app'
    verbose_name = "Плановое техническое обслуживание"