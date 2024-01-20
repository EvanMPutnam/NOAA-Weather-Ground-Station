import collections.abc
from src.utils.singleton import Singleton
from src.common.types import Job
from apscheduler.schedulers.background import BackgroundScheduler
from threading import Lock


@Singleton
class Scheduler:
    def __init__(self):
        self.scheduler_mutex = Lock()
        self.scheduler = BackgroundScheduler()
        self.scheduler.start()

    def job_count(self):
        with self.scheduler_mutex:
            return len(self.scheduler.get_jobs())

    def add_job(self, job: Job, datetime):
        with self.scheduler_mutex:
            self.scheduler.add_job(job, "date", run_date=datetime)

    def add_cron(self, job: Job, hour: int, minute: int):
        with self.scheduler_mutex:
            self.scheduler.add_job(
                job, "cron", day_of_week="mon-sun", hour=hour, minute=minute)

    def shutdown(self):
        with self.scheduler_mutex:
            self.scheduler.shutdown()
