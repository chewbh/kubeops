import pytest

from fastapi.testclient import TestClient
from starlette.config import environ

# set test config
environ["ENV"] = "pytest"


def pytest_runtest_setup(item):
    if "slow" in item.keywords and not item.config.getoption("--runslow"):
        pytest.skip("need --runslow option to run")

    if "incremental" in item.keywords:
        previousfailed = getattr(item.parent, "_previousfailed", None)
        if previousfailed is not None:
            pytest.xfail("previous test failed ({0})".format(
                previousfailed.name))


def pytest_runtest_makereport(item, call):
    if "incremental" in item.keywords:
        if call.excinfo is not None:
            parent = item.parent
            parent._previousfailed = item


@pytest.fixture(scope="session")
def testapp():
    from app.main import app
    yield app


@pytest.fixture(scope="function")
def client(testapp, session, client):
    yield TestClient(testapp)
