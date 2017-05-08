from django.db import models

# an actual node
class Node(models.Model):
    # general stats
    hostname = models.CharField(max_length=20, primary_key=True)
    state = models.CharField(max_length=20)
    # resources
    cpus = models.IntegerField(default=1)
    alloc_cpus = models.IntegerField()
    real_mem = models.IntegerField()
    alloc_mem = models.IntegerField()
    tmp_disk = models.IntegerField()

    def __str__(self):
        return self.hostname


class Job(models.Model):
    # job metadata
    job_id = models.IntegerField(primary_key=True)
    job_state = models.CharField(max_length=20)
    user_id = models.CharField(max_length=20)
    name = models.CharField(max_length=50)
    command = models.CharField(max_length=100)
    submit_time = models.IntegerField()
    start_time = models.IntegerField()  # end time can be calculated using time_limit
    time_limit = models.IntegerField()

    # job allocation details 
    # (allocation per node is assumed identical)
    nodes = models.CharField(max_length=200)
    cpus_per_node = models.IntegerField(default=1)
    mem_per_node = models.IntegerField()

    def __str__(self):
        return str(self.job_id)

