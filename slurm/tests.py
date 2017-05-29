import os
import time
import unittest
from datetime import datetime
from threading import Thread
from multiprocessing.pool import Pool
from multiprocessing import Process

from django.test import TestCase
from django.test.runner import DiscoverRunner
from django.utils import timezone
import redis

import slurm.pyslurm_api as psapi
import slurm.tasks as tasks
from slurm.models import Job
from slurm.dynamic_tables import convert_time

class ProdDBRunner(DiscoverRunner):
    """
    Runs tests on production database in order to handle locks correctly 
    (since everything is a docker container anyways).
    """

    def setup_databases(self, **kwargs):
        pass

    def teardown_databases(self, old_config, **kwargs):
        pass


class GeneralTests(TestCase):

    def test_convert_time_timezone(self):
        """Should have same timezone as server, not UTC"""
        # have at least one job to test with in the db
        os.system('sbatch test-jobs/sleep5.sh')
        tasks.update_jobs() 

        # workaround to get server abbrev.
        test = datetime.fromtimestamp(timezone.now().timestamp(), timezone.get_current_timezone())
        tz = test.strftime('%Z')

        timestamp = Job.objects.all()[0].submit_time
        self.assertTrue(tz in convert_time(timestamp))


class PyslurmApiTest(TestCase):

    def test_ping_controllers_alive(self):
        self.assertTrue(psapi.ping_controllers())


    def test_total_nodes(self):
        self.assertEqual(psapi.total_nodes(), 10)

    
    def test_nodes_reporting(self):
        self.assertEqual(psapi.nodes_reporting(), 10)


class Locks(unittest.TestCase):
    # needs to use unittest.Testcase or it somehow does not use the right Redis
    
    def thread_sleep(self, text, duration):
        with tasks.RedisLock('test_lock'):
            time.sleep(duration)
            redis.Redis().set('test_value', text)


    def test_lock_implementation(self):
        """Make sure our custom locks with Redis work properly"""
        t1 = Thread(target=self.thread_sleep, args=('a', 0.5))
        t2 = Thread(target=self.thread_sleep, args=('b', 0.1))
        t1.start()
        time.sleep(0.1)
        t2.start()
        t1.join()
        t2.join()
        self.assertEqual('b', redis.Redis().get('test_value').decode())
        
    
    def test_lock_implementation2(self):
        """Same as above, but with processes"""
        p1 = Process(target=self.thread_sleep, args=('c', 0.5))
        p2 = Process(target=self.thread_sleep, args=('d', 0.1))
        p1.start()
        time.sleep(0.1)
        p2.start()
        p1.join()
        p2.join()
        self.assertEqual('d', redis.Redis().get('test_value').decode())


    def test_db_lock_handling(self):
        """
        Make sure that we can handle concurrent database updates
        """
        pool = Pool(processes=4)
        res = []
        for p in range(4):
            res.append(pool.apply_async(tasks.update_nodes))
        self.assertTrue(all([p.get() for p in res]))


@unittest.skip
class ControllersAreDeadTest(TestCase):

    @classmethod
    def setUpClass(self):
        # doesn't work the first time for whatever reason
        os.system('killall slurmctld') 


    @classmethod
    def tearDownClass(self):
        os.system('slurmctld')


    def test_ping_controllers_dead(self):
        self.assertFalse(psapi.ping_controllers())


    def test_nodes_reporting(self):
        self.assertEqual(psapi.nodes_reporting(), 0)


