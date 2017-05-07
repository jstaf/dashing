# run with (from project root):
# docker run -h ernie -p 8000:8000 -v$(pwd):/root/dashing -it dashing  

FROM giovtorres/docker-centos7-slurm:latest
MAINTAINER Jeff Stafford <jeff.stafford@queensu.ca>

# install python3 and django
RUN yum makecache fast \
	&& yum -y install python34 python34-pip python34-Cython python34-devel \
	&& pip3 install django ipython

# install pyslurm on python 3
RUN cd ~ \
	&& git clone https://github.com/PySlurm/pyslurm.git \
	&& cd pyslurm \
	&& python3 setup.py build \
	&& python3 setup.py install
    
EXPOSE 8000/tcp

CMD ["/usr/bin/python3", "/root/dashing/manage.py", "runserver", "0.0.0.0:8000"]

