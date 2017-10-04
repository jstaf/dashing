dashing
==================================
A very dashing dashboard for [slurm](slurm.schedmd.com)

Note: this package is currently under development. 
This readme will be updated with actual deployment instructions once it's ready for use.

## Run development environment

This project requires Docker to run the `pyslurm` api and simulate an active SLURM cluster when developing.
Make sure [Docker](https://www.docker.com) is installed. 
Ensure that you've added yourself to the `docker` group to allow using Docker without sudo.

**Run webapp / start a SLURM container**: `snakemake` 
This starts a fake SLURM cluster in a docker container. 
You can view the webapp at `http://localhost:8000/slurm`.

**Start a SLURM bash session** (requires an active SLURM container): `snakemake shell`

**Run tests** (requires an active SLURM container): `snakemake test`

## First time running

Run `snakemake` to build the Docker container, then `Ctrl-C` once it starts and run `snakemake migrate`.
You may need to set SELinux in "permissive" mode if it is running in your dev machine.

## Site customization

To customize the dashboard for your site, edit the files in `slurm/templates/slurm/site` and `slurm/static/slurm`. The timezone is changed in `dashing/settings.py`. Have fun!


