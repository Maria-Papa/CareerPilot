import pytest

pytestmark = pytest.mark.integration


def test_internal_server_error(client):
    @client.app.get("/explode")
    def explode():
        raise RuntimeError("boom")

    with pytest.raises(RuntimeError):
        client.get("/explode")
