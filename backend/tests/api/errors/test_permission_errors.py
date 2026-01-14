import pytest
from fastapi import Depends, HTTPException
from tests.utils.api_assertions import assert_403

pytestmark = pytest.mark.integration


def test_permission_denied(client):
    # Create a dummy dependency that always denies access
    def deny():
        raise HTTPException(status_code=403, detail="Forbidden")

    # Add a temporary protected route
    @client.app.get("/protected", dependencies=[Depends(deny)])
    def protected():
        return {"ok": True}

    resp = client.get("/protected")
    assert_403(resp)
    assert resp.json()["detail"] == "Forbidden"
