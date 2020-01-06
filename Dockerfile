# Dockerfile
FROM python:3.7

COPY killrvideo/ requirements.txt /app/
WORKDIR /app

# Install app dependencies
RUN pip install -r requirements.txt \
    && python -m nltk.downloader stopwords

# Create app directory
ENV PYTHONPATH "${PYTHONPATH}:/${WORKDIR}"

EXPOSE 50101
 
CMD ["python", "./__init__.py"]
