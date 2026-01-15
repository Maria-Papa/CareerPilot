import pytest
from fastapi.testclient import TestClient
from tests.utils.api_assertions import assert_422

pytestmark = pytest.mark.integration


def test_create_company_validation_error(client: TestClient) -> None:
    # Missing required field "name"
    payload = {"website": "https://example.com", "industry": "Tech"}

    resp = client.post("/companies", json=payload)
    assert_422(resp)

    body = resp.json()
    assert body["detail"][0]["loc"][-1] == "name"
    assert body["detail"][0]["msg"]  # FastAPI/Pydantic error message
