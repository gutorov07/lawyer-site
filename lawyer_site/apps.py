from django.apps import AppConfig

class LawyerSiteConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'lawyer_site'  # ← должно быть именно так