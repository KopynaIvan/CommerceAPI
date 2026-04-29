from celery import Celery
import os

celery_app = Celery("worker",
                    broker=os.environ.get("REDIS_URL", "redis://redis:6379/0"),
                    backend=os.environ.get("REDIS_URL", "redis://redis:6379/0"))

