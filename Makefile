.PHONY = run, shell, clean

# run docker container
run: docker/image.token
	docker run -h ernie -p 8000:8000 -v $(shell pwd):/root/dashing -it dashing

# attach to running docker container
shell:
	docker exec -it $(shell docker ps | awk '$$2 == "dashing" {print $$1}') bash

# force rebuild of docker container
clean:
	rm -f docker/image.token

# build docker container
docker/image.token: docker/Dockerfile 
	docker build -t dashing docker/
	touch $@


