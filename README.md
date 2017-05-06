dashing
==================================
An admin/stats dashboard for the SLURM Workload Manager

## Run development environment

* Install Miniconda 3 from [https://conda.io/miniconda.html](https://conda.io/miniconda.html)
* Recreate Conda environment / install required packages: `conda env create -f environment.yml`
* Make sure [Docker](https://www.docker.com) is installed. Docker is necessary to run an imaginary SLURM cluster to test with.
* `make` and go to `localhost:8000` in a browser. You can SSH into the box and run jobs/etc at port 2222.


