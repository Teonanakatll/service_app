

from .celery_app import app as celery_app

# чтобы celery стартовал вместе с джанго проектом
__all__ = ('celery_app',)