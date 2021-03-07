import logging
from tabulate import tabulate

from fastapi import FastAPI
from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import RedirectResponse
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint

from .api import api_router, URI_PREFIX_API, URI_PREFIX_API_DOCS, LATEST_API_VERSION
from .logging import configure_logging
from .monitoring import metrics_instrumentation

# configure logging and log level
log = logging.getLogger(__name__)
configure_logging()

# asgi, routers and api
app = FastAPI(docs_url=None, redoc_url=None, openapi_url=None)

@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    """Add header indicating should only be accessed using HTTPS"""
    response = await call_next(request)
    response.headers["Strict-Transport-Security"] = "max-age=31536000 ; includeSubDomains"
    return response


@app.get("/")
def root():
    return RedirectResponse(url=f'/{URI_PREFIX_API}/{LATEST_API_VERSION}/{URI_PREFIX_API_DOCS}')


@app.get("/healthz", include_in_schema=False)
def healthcheck():
    return {"status": "ok"}


app.include_router(api_router, prefix=f"/{URI_PREFIX_API}")

# add metrics instrumentation and integration
metrics_instrumentation(app)

# list all registered API routes to the console
# NOTE: this is printed once per uvicorn worker (default is 2)
table = []
for route in api_router.routes:
    table.append([f"/{URI_PREFIX_API}{route.path}",
                  route.name, ",".join(route.methods)])

log.debug("Available Endpoints \n" +
          tabulate(table, headers=["Path", "Name", "Methods"]))
