from typing import cast

import pytest
from app.core.errors import EntityNotFoundError
from fastapi import FastAPI
from fastapi.testclient import TestClient
from tests.utils.api_assertions import assert_404

pytestmark = pytest.mark.integration


def test_entity_not_found_handler(client: TestClient) -> None:
    app = cast(FastAPI, client.app)

    raise_error = lambda: (_ for _ in ()).throw(EntityNotFoundError("missing"))

    @app.get("/force404")
    def force():
        raise_error()

    resp = client.get("/force404")
    assert_404(resp)
    assert "missing" in resp.json()["detail"]
