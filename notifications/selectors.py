from notifications.models import Notification


def get_notifications(user, filters=None):
    queryset = Notification.objects.for_recipient(user)

    if filters:
        if filters.get("is_read") is not None:
            is_read = filters["is_read"].lower() == "true"
            queryset = queryset.filter(is_read=is_read)

        if filters.get("type"):
            queryset = queryset.filter(type=filters["type"])

    return queryset

