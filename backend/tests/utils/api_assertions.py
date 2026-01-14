def assert_status(resp, expected):
    assert resp.status_code == expected, f"Expected {expected}, got {resp.status_code}"


def assert_json_keys(resp, *keys):
    data = resp.json()
    for key in keys:
        assert key in data, f"Missing key '{key}' in response JSON"


def assert_404(resp):
    assert_status(resp, 404)
    assert "detail" in resp.json()


def assert_403(resp):
    assert_status(resp, 403)
    assert "detail" in resp.json()


def assert_400(resp):
    assert_status(resp, 400)
    assert "detail" in resp.json()


def assert_422(resp):
    assert_status(resp, 422)
    assert "detail" in resp.json()


def assert_list(resp):
    assert isinstance(resp.json(), list), "Expected JSON list"
