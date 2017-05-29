# run with (from project root):
# docker run -h ernie -p 8000:8000 -v$(pwd):/root/dashing -it dashing  

FROM giovtorres/docker-centos7-slurm:latest
MAINTAINER Jeff Stafford <jeff.stafford@queensu.ca>

# install python3 and django
RUN yum makecache fast \
	&& yum -y install python34 python34-pip python34-Cython python34-devel python34-numpy redis
RUN pip3 install django ipython snakemake celery redis

# install pyslurm on python 3
RUN cd ~ \
	&& git clone https://github.com/PySlurm/pyslurm.git \
	&& cd pyslurm \
	&& python3 setup.py build \
	&& python3 setup.py install
   
EXPOSE 8000/tcp

WORKDIR '/root/dashing'

CMD ["./docker/start-server.sh"]

