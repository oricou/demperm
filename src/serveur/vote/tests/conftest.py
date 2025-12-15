import os
import sys
from pathlib import Path

import django
import pytest

BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app.settings")
django.setup()

@pytest.fixture(autouse=True)
def override_authentication(settings):
    settings.REST_FRAMEWORK["DEFAULT_AUTHENTICATION_CLASSES"] = [
        "tests.fake_authentication.FakeAuthentication"
    ]