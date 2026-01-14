import pytest
from app.core.errors import (
    AccessDeniedError,
    ConflictError,
    DomainError,
    EntityNotFoundError,
    ValidationError,
)
from tests.utils.api_assertions import (
    assert_400,
    assert_403,
    assert_404,
    assert_status,
)

pytestmark = pytest.mark.integration


def test_entity_not_found_handler(client):
    @client.app.get("/force404")
    def force():
        raise EntityNotFoundError("missing")

    resp = client.get("/force404")
    assert_404(resp)
    assert resp.json()["detail"] == "missing"


def test_conflict_error_handler(client):
    @client.app.get("/force409")
    def force():
        raise ConflictError("duplicate")

    resp = client.get("/force409")
    assert_status(resp, 409)
    assert resp.json()["detail"] == "duplicate"


def test_access_denied_error_handler(client):
    @client.app.get("/force403")
    def force():
        raise AccessDeniedError("no access")

    resp = client.get("/force403")
    assert_403(resp)
    assert resp.json()["detail"] == "no access"


def test_domain_validation_error_handler(client):
    @client.app.get("/force400")
    def force():
        raise ValidationError("invalid state")

    resp = client.get("/force400")
    assert_400(resp)
    assert resp.json()["detail"] == "invalid state"


def test_generic_domain_error_handler(client):
    @client.app.get("/force400-generic")
    def force():
        raise DomainError("generic domain failure")

    resp = client.get("/force400-generic")
    assert_400(resp)
    assert resp.json()["detail"] == "generic domain failure"
