# core/channel_layer.py

import logging
import redis
from django.conf import settings

logger = logging.getLogger(__name__)


def get_channel_layer_config():
    try:
        client = redis.Redis.from_url(
            settings.REDIS_URL,
            socket_connect_timeout=2,
            socket_timeout=2,
        )
        client.ping()

        logger.info("Redis Channel Layer Enabled")

        return {
            "default": {
                "BACKEND": "channels_redis.core.RedisChannelLayer",
                "CONFIG": {
                    "hosts": [settings.REDIS_URL],
                },
            }
        }

    except Exception as e:
        logger.warning(f"Redis unavailable. Using InMemoryChannelLayer. Error: {e}")

        return {
            "default": {
                "BACKEND": "channels.layers.InMemoryChannelLayer",
            }
        }