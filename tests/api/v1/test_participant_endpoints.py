from fastapi import status


def test_health(client):
    resp = client.get("/health")
    assert resp.status_code == status.HTTP_200_OK
    assert resp.json() == {"status": "ok"}


def test_crud_flow(client):
    # Create
    create_data = {"name": "RT", "email": "rt@example.com"}
    resp = client.post("/participants/", json=create_data)
    assert resp.status_code == status.HTTP_200_OK
    data = resp.json()
    pid = data["id"]
    assert data["name"] == "RT"
    assert data["email"] == "rt@example.com"

    # Read
    resp = client.get(f"/participants/{pid}")
    assert resp.status_code == status.HTTP_200_OK
    assert resp.json()["id"] == pid

    # List
    resp = client.get("/participants/")
    assert resp.status_code == status.HTTP_200_OK
    assert isinstance(resp.json(), list)

    # Patch
    resp = client.patch(f"/participants/{pid}", json={"email": "rt2@example.com"})
    assert resp.status_code == status.HTTP_200_OK
    assert resp.json()["email"] == "rt2@example.com"

    # Delete
    resp = client.delete(f"/participants/{pid}")
    assert resp.status_code == status.HTTP_200_OK
    # Ensure 404 afterwards
    resp = client.get(f"/participants/{pid}")
    assert resp.status_code == status.HTTP_404_NOT_FOUND


def test_errors(client):
    # 404 on missing
    resp = client.get("/participants/9999")
    assert resp.status_code == status.HTTP_404_NOT_FOUND

    # 422 on bad patch payload
    create_data = {"name": "ERR", "email": "err@example.com"}
    resp = client.post("/participants/", json=create_data)
    pid = resp.json()["id"]
    bad = client.patch(f"/participants/{pid}", json={"email": 123})
    assert bad.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
