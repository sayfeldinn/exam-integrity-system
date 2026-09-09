"""Export OpenAPI schema from the running FastAPI app.

Usage:
    python packages/shared/export_openapi.py > docs/openapi.json

Requires the api service dependencies to be installed.
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "services" / "api"))

from main import app  # noqa: E402

schema = app.openapi()
print(json.dumps(schema, indent=2))
