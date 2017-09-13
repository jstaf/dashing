from django.db import models

class Node(models.Model):
    """Per-node stats"""
    # general stats
    hostname = models.CharField(max_length=20, primary_key=True)
    state = models.CharField(max_length=20)
    # resources
    cpus = models.IntegerField(default=1)
    alloc_cpus = models.IntegerField()
    real_mem = models.IntegerField()
    alloc_mem = models.IntegerField()

    def __str__(self):
        return self.hostname


class Job(models.Model):
    """Per-job stats"""
    # job metadata
    job_id = models.IntegerField(primary_key=True)
    job_state = models.CharField(max_length=20)
    user_id = models.CharField(max_length=20)
    name = models.CharField(max_length=50)
    submit_time = models.DateTimeField()
    start_time = models.DateTimeField(null=True)  # end time can be calculated using time_limit
    time_limit = models.IntegerField(null=True)
    # job allocation details (allocation per node is assumed identical)
    nodes = models.CharField(max_length=100, null=True)
    cpus_per_node = models.IntegerField(default=1)
    mem_per_node = models.IntegerField()

    def __str__(self):
        return str(self.job_id)


class ClusterSnapshot(models.Model):
    """Cluster "over-time" statistics"""
    time = models.DateTimeField(auto_now=True, primary_key=True)
    slurmctld_alive = models.IntegerField(default=0)
    nodes_total = models.IntegerField()
    nodes_alive = models.IntegerField()
    nodes_alloc = models.IntegerField()
    jobs_running = models.IntegerField()
    jobs_pending = models.IntegerField()
    jobs_other = models.IntegerField()
    jobs_avg_qtime = models.DurationField()
    cpus_total = models.IntegerField()
    cpus_alloc = models.IntegerField()

    def __str__(self):
        return str(self.time)
