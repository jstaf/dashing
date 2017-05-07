import os
import time
import unittest

from django.test import TestCase

import slurm.pyslurm_api as psapi 

class PyslurmApiTest(TestCase):

    def test_ping_controllers_alive(self):
        self.assertTrue(psapi.ping_controllers())


    def test_total_nodes(self):
        self.assertEqual(psapi.total_nodes(), 10)

    
    def test_nodes_reporting(self):
        self.assertEqual(psapi.nodes_reporting(), 10)


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


