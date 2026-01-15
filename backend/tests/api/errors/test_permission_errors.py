from typing import cast

import pytest
from fastapi import Depends, FastAPI, HTTPException
from fastapi.testclient import TestClient
from tests.utils.api_assertions import assert_403

pytestmark = pytest.mark.integration


def test_permission_denied(client: TestClient) -> None:
    app = cast(FastAPI, client.app)

    def deny():
        raise HTTPException(status_code=403, detail="Forbidden")

    @app.get("/protected", dependencies=[Depends(deny)])
    def protected():
        return {"ok": True}

    resp = client.get("/protected")
    assert_403(resp)
    assert resp.json()["detail"] == "Forbidden"
