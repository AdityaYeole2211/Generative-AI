from rq import Queue
from redis import Redis

queue = Queue(connection=Redis(host= 'valkey'))
