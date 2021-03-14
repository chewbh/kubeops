FROM python:3.9-buster AS build-base

# Sane defaults for pip and python
ENV \
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=1 \
  PYTHONUNBUFFERED=1

# copy the dependencies file and install app dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# ---

ARG NOCACHE=0
FROM build-base AS test

# COPY --from=base /usr/local/lib/python3.9/site-packages/ /usr/local/lib/python3.9/site-packages/

# RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir "pytest" "requests"

# copy test src
COPY tests/ ./tests

# copy the content of the local src
COPY src/ .

# run from test directory
WORKDIR /tests

# workaround to skip layer caching to ensure
# test are always run in build
ARG NOCACHE

# test is run as part of image build
RUN [ "pytest" ]

# ---

FROM build-base AS release
RUN pip install --no-cache-dir "uvicorn[standard]" gunicorn

# copy the content of the local src
COPY src/ .

EXPOSE 80

CMD [ "gunicorn", "-k" , "uvicorn.workers.UvicornWorker", "-c", "/gunicorn_conf.py", "app.main:app" ]
