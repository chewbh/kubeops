FROM python:3.9-buster

# Sane defaults for pip
ENV \
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=1

# copy the dependencies file and install dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir "uvicorn[standard]" gunicorn && \
  pip install --no-cache-dir -r requirements.txt

# copy the content of the local src
COPY src/ .

EXPOSE 80

CMD [ "gunicorn", "-k" , "uvicorn.workers.UvicornWorker", "-c", "/gunicorn_conf.py", "app.main:app" ]
