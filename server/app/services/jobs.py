import os
import redis
from rq import Queue, Retry


REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379")
conn = redis.from_url(REDIS_URL)
queue = Queue(connection=conn)
dead_letter_queue = Queue("failed", connection=conn)


def enqueue_request(request_id: int):
    from worker.tasks import process_request

    # Retry up to 3 times, 10s, 60s, 300s between attempts
    retry_strategy = Retry(max=3, interval=[10, 60, 300])
    job = queue.enqueue(process_request, request_id, retry=retry_strategy)


def process_dead_letter_queue(log_failed: bool = True, requeue: bool = False):
    """
    Process jobs in the dead-letter (failed) queue.
    If log_failed is True, log job info and exception.
    If requeue is True, requeue the job to the main queue.
    """
    failed_jobs = dead_letter_queue.get_jobs()
    for job in failed_jobs:
        if log_failed:
            print(f"[DEAD-LETTER] Job {job.id} failed: {job.exc_info}")
        if requeue:
            job.requeue(queue)
            print(f"[DEAD-LETTER] Job {job.id} requeued to main queue.")
