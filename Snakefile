# because makefiles actually suck for doing anything complex

import os

DASHING_LOC = '/root/dashing'

def docker_run(command):
	"""Run a command in the SLURM Docker container"""
	os.system("""docker exec -it $(docker ps | awk '$2 == "dashing" {print $1}') %s""" % command)


# run docker container
rule run:
	input: 	'tokens/docker_image.tkn'
	shell: 	'docker run -h ernie -p 8000:8000 -v $(pwd):%s -it dashing' % DASHING_LOC


# attach to running docker container
rule shell:
	run: 	
		docker_run('bash')


# start an ipython shell in the container
rule pyshell:
	run:
		docker_run('python3 manage.py shell')


# run unit tests
rule test:
	run: 	
		docker_run('python3 manage.py test slurm')


# perform any initialization that needs to happen
rule init:
	output:	'tokens/init.tkn'
	run:
		os.system('snakemake migrate')
		docker_run('python3 manage.py createsuperuser')
		os.system('touch %s' % output[0])

# perform db migration
rule migrate:
	run:
		docker_run('python3 manage.py makemigrations')
		docker_run('python3 manage.py migrate')


# build docker container
rule docker_build:
	input:  'docker/Dockerfile'
	output: 'tokens/docker_image.tkn'
	shell: 
		'''
		docker build -t dashing docker/
		touch {output}
		'''

# nuke all tempfiles for starting over
rule clean:
	shell:
		'''
		rm -rf tokens/
		rm -f db.sqlite3
		'''

