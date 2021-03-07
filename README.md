# KubeOps

JSD (Jira Service Desk) webhook for gitops based automation on kubernetes cluster

## What is KubeOps

KubeOps is a REST based API that automate administration tasks on given kubernetes clusters. It is implemented on [FastAPI](https://fastapi.tiangolo.com).

Adopting a gitops approach, task execution is done by generating relevant `kubernetes manifest` and committing changes into a git repo, when trigger CI/CD pipeline to perform actual change on the kubernetes cluster.

## API Design and OpenAPI Documentation

APIs are REST based, and prefix with `/api`. Details on the APIs can be found on the Swagger UI, which is generated using OpenAPI specification.

In addition, the index page of the app will redirect to the OpenAPI documentation of the last api version. Otherwise, the documentation of a given api version can be access via http://`app-domain-uri`/api/`api version (e.g. v1)`/docs

## Configuration

KubeOps follows the [twelve-factor methodology](https://12factor.net/), and thus, it uses environment variables as the sole mean for app configuration.

### Web Server

Based on [FastAPI](https://fastapi.tiangolo.com), the app run on `Gunicorn` (a mature and fully featured python web server) with the `Uvicorn` worker class. `Uvicorn` workers is ASGI based, which enable the running of asynchronous Python web code.

The default setup, which is adapted from **`tiangolo/uvicorn-gunicorn-fastapi-docker`** docker image, is meant for production deployment with performance auto-tuning for typical FastAPI based app in Python 3.x such as KubeOps.

The achievable performance is on par with (and in many cases superior to) Go and Node.js frameworks.

If needed, specific custom configuration to both `Gunicorn` and `Uvicorn` can be done via modifying `gunicorn_conf.py` directly in the src directory. This is not necessary or recommended in most cases.

| Environment | Default | Description |
|-------------|---------|-------------|
| WORKERS_PER_CORE | 1 | Number of uvicorn workers to spawn per vCPU |
| MAX_WORKERS | - | Maximum numer of uvicorn workers |
| WEB_CONCURRENCY | 2 | Actual number of uvicorn workers to spawn. If not set, this is determined based on `WORKERS_PER_CORE` and `MAX_WORKERS`. Min. default is 2 |
| HOST | 0.0.0.0 | Host to bind |
| PORT | 80 | Port number to bind |
| BIND | - | The socket to bind |
| GUNICORN_LOG_LEVEL | INFO | Log level for specific to web server. It may differs from app's log level |
| ACCESS_LOG | - | The Access log file to write to. Default '-'  means log to stdout |
| ERROR_LOG | - | The Error log file to write to. Default '-'  means log to stderr |
| GRACEFUL_TIMEOUT | 120 | Timeout for graceful workers restart. |
| TIMEOUT | 120 | Workers silent for more than this many seconds are killed and restarted. |
| KEEP_ALIVE | 5 | The number of seconds to wait for requests on a Keep-Alive connection. |

### Monitoring

For observabililty, the app support metrics instrumentation for  prometheus. This is done using [Prometheus FastAPI Instrumentator](https://pypi.org/project/prometheus-fastapi-instrumentator/).

For custom metrics, it can be added to the instrumentator located in `monitoring.py` in the src directory.

Note that `ENABLE_METRICS` must be set to `true` in order for the metrics to be exposed on the uri `/metrics`.

| Environment | Default | Description |
|-------------|---------|-------------|
| ENABLE_METRICS | - | Set to `true` to expose prometheus metrics endpoint. Default is not to expose endpoint.  |

### Logging

Logs from `Gunicorn` and app are configured to follow the same log format so that it can be easily read or exploited in tools such as Elastic Stack.

Structured logging is incorporated in the app and can be switched easily via setting `JSON_LOGS` to `1`.

`Fluentd` can be further used to pipe logs from multiple instances of the app to a elasticsearch for centralized logging.

| Environment | Default | Description |
|-------------|---------|-------------|
| LOG_LEVEL | WARN | Default log level for the app |
| JSON_LOGS | 0 |

### Other Environment Variables

| Environment | Default | Description |
|-------------|---------|-------------|
| ENV | local | Environment. Set to `production` to indicate production deployment or `pytest` for testing |
| ENV_TAGS | - | List of environment-tags pairs |
| APP_UI_URL | - | uri of app when the fqdn of the app differs default use of reverse proxy or DNS CNAME |
| SECRET_PROVIDER | - | secret provider to use. Default uses `secret` in starlette |

## Installation and Running

KubeOps will run in a OCI container, and that is built using `docker`, `docker-compose`, and `make`. See the command below:

```bash

# build container image
make build

# run the app using docker-compose
make run && docker-compose logs -f
```
