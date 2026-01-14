import pytest
from app.core.errors import ConflictError
from tests.utils.api_assertions import assert_status

pytestmark = pytest.mark.integration


def test_service_conflict_error_propagates_to_handler(client):
    @client.app.get("/service-conflict")
    def route():
        raise ConflictError("duplicate name")

    resp = client.get("/service-conflict")
    assert_status(resp, 409)
    assert resp.json()["detail"] == "duplicate name"
