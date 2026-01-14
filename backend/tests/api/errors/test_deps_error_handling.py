import pytest
from fastapi import Depends
from tests.utils.api_assertions import assert_404

pytestmark = pytest.mark.integration


def test_get_entity_or_404_dependency(client):
    def fake_getter(session, id):
        return None  # simulate missing entity

    from app.api.deps import get_entity_or_404

    dep = get_entity_or_404(fake_getter)

    @client.app.get("/dep404")
    def route(entity=Depends(dep)):
        return {"ok": True}

    resp = client.get("/dep404?company_id=1")
    assert_404(resp)
