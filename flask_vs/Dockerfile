FROM tiangolo/uwsgi-nginx-flask:flask-python3.5
ADD ./app/requirments.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt
COPY ./app /app
WORKDIR /app


