import os
import redis
from rq import Worker, Queue
from dotenv import load_dotenv

load_dotenv()

listen = ['default']
redis_url = os.getenv('REDIS_URL', 'redis://redis:6379' or 'redis://localhost:6379')

conn = redis.from_url(redis_url)
queue = Queue(connection=conn)

if __name__ == '__main__':
    queues = [Queue(name, connection=conn) for name in listen]
    worker = Worker(queues, connection=conn)
    worker.work()
