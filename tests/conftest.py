from pathlib import Path

import pytest

FIXTURES = Path(__file__).parent / "fixtures"


@pytest.fixture
def access_log() -> Path:
    return FIXTURES / "access.log"


@pytest.fixture
def auth_log() -> Path:
    return FIXTURES / "auth.log"
