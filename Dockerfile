FROM python:3.8
ENV PYTHONUNBUFFERED=1
WORKDIR /kalimba
COPY requirements.txt requirements.txt
RUN apt-get update && apt-get install -y netcat
RUN python -m pip install --upgrade pip
RUN pip3 install -r requirements.txt