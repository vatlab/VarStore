FROM hail_dp:latest
ADD ./app/requirments.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt
COPY ./app /app
WORKDIR /app

