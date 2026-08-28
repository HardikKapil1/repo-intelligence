from redis import Redis
from rq import Queue

from app.core.config import settings

redis_connection = Redis.from_url(
    settings.redis_url,
)

ingestion_queue = Queue(
    "ingestion",
    connection=redis_connection,
)
