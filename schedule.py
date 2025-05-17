import datetime
import time

_jobs = []

class Job:
    def __init__(self, at_time):
        self.at_time = at_time
        self.job_func = None
        self.last_run = None

    def do(self, func):
        self.job_func = func
        _jobs.append(self)
        return self

class Every:
    def day(self):
        return Day()

class Day:
    def at(self, time_str):
        hour, minute = map(int, time_str.split(':'))
        at_time = datetime.time(hour, minute)
        return Job(at_time)


def every():
    return Every()


def run_pending():
    now = datetime.datetime.now()
    for job in list(_jobs):
        target = datetime.datetime.combine(now.date(), job.at_time)
        if now >= target and (job.last_run is None or job.last_run.date() < now.date()):
            job.job_func()
            job.last_run = now

