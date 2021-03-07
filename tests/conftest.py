import pytest

from starlette.testclient import TestClient
from starlette.config import environ

# set test config
environ["ENV"] = "pytest"
