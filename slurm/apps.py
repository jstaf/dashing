from django.apps import AppConfig

class SlurmConfig(AppConfig):
    name = 'slurm'

    def ready(self):
        # unlock the database in case of a non-smooth exit from last time
        from .tasks import RedisLock
        RedisLock('db').release()
