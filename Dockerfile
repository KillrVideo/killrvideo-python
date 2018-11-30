# Dockerfile
FROM python:3.6-alpine

ARG KILLRVIDEO_DOCKER_IP
ENV KILLRVIDEO_DOCKER_IP ${KILLRVIDEO_DOCKER_IP}

ARG KILLRVIDEO_HOST_IP
ENV KILLRVIDEO_HOST_IP ${KILLRVIDEO_HOST_IP}

ARG KILLRVIDEO_DSE_USERNAME
ENV KILLRVIDEO_DSE_USERNAME ${KILLRVIDEO_DSE_USERNAME}

ARG KILLRVIDEO_DSE_PASSWORD
ENV KILLRVIDEO_DSE_PASSWORD ${KILLRVIDEO_DSE_PASSWORD}

# Install app dependencies
RUN pip install grpc
RUN pip install python-etcd

# Create app directory
COPY killrvideo/ /app
WORKDIR /app

EXPOSE 8899
 
CMD ["gunicorn", "-w 4", "main:app"]
