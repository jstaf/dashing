import os
import unittest
from multiprocessing.pool import Pool

from django.test import TestCase
from django.test.runner import DiscoverRunner

import slurm.pyslurm_api as psapi
import slurm.tasks as tasks

class ProdDBRunner(DiscoverRunner):
    """
    Runs tests on production database in order to handle locks correctly 
    and since everything is a docker container anyways
    """

    def setup_databases(self, **kwargs):
        pass

    def teardown_databases(self, old_config, **kwargs):
        pass


class PyslurmApiTest(TestCase):

    def test_ping_controllers_alive(self):
        self.assertTrue(psapi.ping_controllers())


    def test_total_nodes(self):
        self.assertEqual(psapi.total_nodes(), 10)

    
    def test_nodes_reporting(self):
        self.assertEqual(psapi.nodes_reporting(), 10)


    def test_db_lock_handling(self):
        """
        Make sure that we can handle conccurent database updates
        """
        pool = Pool(processes=10)
        res = []
        for p in range(10):
            res.append(pool.apply_async(tasks.update_nodes))
        print(list(map(lambda x: x.get(), res)))
        self.assertTrue(all([x.get() for x in res]))


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


