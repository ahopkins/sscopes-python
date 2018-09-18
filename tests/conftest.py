import pytest
from collections import namedtuple


@pytest.fixture
def ScopeTestCase():
    yield namedtuple("ScopeTestCase", ["base", "inbound", "outcome"])
