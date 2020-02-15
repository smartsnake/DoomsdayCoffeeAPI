FROM python:3.8
ADD . /app
WORKDIR /app
EXPOSE 5000
RUN pip install -r requirements.txt