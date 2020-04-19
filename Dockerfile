FROM python:3.8.2-alpine3.11
ADD requirements.txt /app/
WORKDIR /app
RUN pip install -r requirements.txt
ADD wsgi.py /app/
ADD tfstated /app/tfstated
CMD ["gunicorn", "--access-logfile", "-", "-b", "0.0.0.0", "wsgi"]
