import os
import redis
from rq import Queue

REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379")
conn = redis.from_url(REDIS_URL)
queue = Queue(connection=conn)

def enqueue_request(request_id: int):
    from worker.tasks import process_request
    queue.enqueue(process_request, request_id)
