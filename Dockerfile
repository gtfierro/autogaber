FROM ubuntu

RUN apt-get update
RUN apt-get install -y python-setuptools build-essential python-dev mercurial vim openssh-server python-pip
RUN pip install ipython
RUN wget http://fierro.me/data/indiegogo_subset.json

#ADD <src> <dst> # to copy over a file into the docker container

#Usage: docker insert IMAGE URL PATH
#
#Insert a file from URL in the IMAGE at PATH
