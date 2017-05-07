import os
import time

from django.test import TestCase

import slurm.pyslurm_api as psapi 

class PyslurmApiTest(TestCase):

    def test_ping_controllers_alive(self):
        self.assertIs(psapi.ping_controllers(), True)



class ControllersAreDeadTest(TestCase):

    @classmethod
    def setUpClass(self):
        os.system('killall slurmctld')  # aaaahhhh


    @classmethod
    def tearDownClass(self):
        os.system('slurmctld')
        time.sleep(10)  # give slurmctld time to restart


    def test_ping_controllers_dead(self):
        self.assertIs(psapi.ping_controllers(), False)

