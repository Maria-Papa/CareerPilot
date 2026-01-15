from typing import cast

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

pytestmark = pytest.mark.integration


def test_internal_server_error(client: TestClient) -> None:
    app = cast(FastAPI, client.app)

    @app.get("/explode")
    def explode():
        raise RuntimeError("boom")

    with pytest.raises(RuntimeError):
        client.get("/explode")
