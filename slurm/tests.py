import os
import time

from django.test import TestCase

import slurm.pyslurm_api as psapi 

class PyslurmApiTest(TestCase):

    def test_ping_controllers_alive(self):
        self.assertIs(psapi.ping_controllers(), True)


    def test_ping_controllers_dead(self):
        os.system('killall slurmctld')  # aaaahhhh
        self.assertIs(psapi.ping_controllers(), False)
        os.system('slurmctld &')
        time.sleep(5)  # give slurmctl 5 seconds to restart

