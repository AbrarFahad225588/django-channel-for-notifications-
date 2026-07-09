from django.utils import timezone


def now_iso():
    return timezone.now().isoformat()
