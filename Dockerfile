FROM python:3.8.1
ADD . /app
WORKDIR /app
EXPOSE 5000
RUN pip install -r requirements.txt
RUN pip install gunicorn
CMD [ "gunicorn", "-w", "4", "--bind", "0.0.0.0:5000", "wsgi"]