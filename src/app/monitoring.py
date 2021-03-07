from typing import Callable

from prometheus_client import Histogram, Counter
from prometheus_fastapi_instrumentator import Instrumentator, metrics
from prometheus_fastapi_instrumentator.metrics import Info


instrumentator = Instrumentator(
    should_group_status_codes=False,
    should_ignore_untemplated=True,
    should_respect_env_var=True,
    should_instrument_requests_inprogress=True,
    excluded_handlers=[".*admin.*", "/metrics", "/healthz"],
    env_var_name="ENABLE_METRICS",
    inprogress_name="inprogress",
    inprogress_labels=True,
)


def metrics_instrumentation(fast_api_app):
    instrumentator.instrument(fast_api_app).expose(
        fast_api_app,
        include_in_schema=False,
        should_gzip=False)

# ----- custom metrics -----
