from django.apps import AppConfig


class SubscriptionsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "subscriptions"

    def ready(self):
        from django.db.models.signals import post_migrate
        from subscriptions import signals

        post_migrate.connect(signals.seed_default_plans, sender=self)
