.PHONY = run, shell, migrate, test

# run docker container
run: tokens/docker_image.tkn tokens/init.tkn
	docker run -h ernie -p 8000:8000 -v $(shell pwd):/root/dashing -it dashing

# attach to running docker container
shell:
	docker exec -it $(shell docker ps | awk '$$2 == "dashing" {print $$1}') bash

# run automated tests using docker container
test:
	docker exec -it $(shell docker ps | awk '$$2 == "dashing"     {print $$1}') python3 /root/dashing/manage.py test slurm

# run all commands necessary to intialize django
init: tokens/init.tkn

tokens/init.tkn: 
	mkdir -p tokens
	make migrate
	python3 manage.py createsuperuser
	touch $@

# perform migration if necessary
migration:
	docker exec -it $(shell docker ps | awk '$$2 == "dashing"     {print $$1}') python3 /root/dashing/manage.py makemigrations
	docker exec -it $(shell docker ps | awk '$$2 == "dashing"     {print $$1}') python3 /root/dashing/manage.py migrate

# build docker container
tokens/docker_image.tkn: docker/Dockerfile 
	mkdir -p tokens
	docker build -t dashing docker/
	touch $@


