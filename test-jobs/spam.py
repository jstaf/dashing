#!/usr/bin/env python3
"""
A super quick-and-dirty job submission wrapper to submit a bunch of test jobs at once.
"""

import os
import sys

for i in range(int(sys.argv[1])):
    os.system('sbatch test-jobs/sleep5.sh')
