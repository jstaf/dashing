.PHONY = run, shell, migrate

# run docker container
run: tokens/docker_image.tkn tokens/init.tkn
	docker run -h ernie -p 8000:8000 -v $(shell pwd):/root/dashing -it dashing

# attach to running docker container
shell:
	docker exec -it $(shell docker ps | awk '$$2 == "dashing" {print $$1}') bash

# run all commands necessary to intialize django
init: tokens/init.tkn

tokens/init.tkn: 
	mkdir -p tokens
	make migrate
	python3 manage.py createsuperuser
	touch $@

# perform migration if necessary
migrate:
	python3 manage.py makemigrations
	python3 manage.py migrate

# build docker container
tokens/docker_image.tkn: docker/Dockerfile 
	mkdir -p tokens
	docker build -t dashing docker/
	touch $@


