FROM ubuntu:18.04

RUN apt-get update -y
RUN apt-get update --fix-missing

RUN apt-get install python3 -y
RUN apt-get install python3-pip -y
RUN apt-get install apache2 -y
RUN apt-get install redis-server -y

RUN python3 -m pip install redis

# for debugging. 
#RUN apt-get install net-tools -y
#RUN apt-get install vim -y

# you should change this whatever is appropriate on your machine.
WORKDIR /home/derek/Desktop/rollcall

# Apache port 
EXPOSE 80

COPY rollcall.py /usr/lib/cgi-bin
COPY ./start.sh .

CMD ["sh", "start.sh"]
