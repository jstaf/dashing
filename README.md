dashing
==================================
An admin/stats dashboard for the SLURM Workload Manager

## Run development environment

This project requires Docker to run the `pyslurm` api and simulate an active SLURM cluster when developing.
Make sure [Docker](https://www.docker.com) is installed. 
Ensure that you've added yourself to the `docker` group to allow using Docker without sudo.

**Run webapp / start a SLURM container**: `snakemake` 
This starts a fake SLURM cluster in a docker container. 
You can view the webapp at `http://localhost:8000/slurm`.

**Start a SLURM bash session** (requires an active SLURM container): `snakemake shell`

**Run tests** (requires an active SLURM container): `snakemake test`

