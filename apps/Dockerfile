FROM python:3.8-slim-buster
WORKDIR /python-docker
COPY requirements.txt requirements.txt
RUN apt update
RUN apt-get install python3-dev default-libmysqlclient-dev build-essential -y
RUN pip3 install -r requirements.txt
COPY init_db.py /python-docker/
ENV DB_USERNAME postgres
ENV DB_PASSWORD sgn
RUN python3 init_db.py
COPY /src /python-docker
CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]