FROM python:3.9

WORKDIR /app

COPY ./app/requirements.txt /app/app/
RUN pip install --upgrade pip
RUN pip install -r app/requirements.txt
