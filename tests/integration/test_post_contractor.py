# tests/integration/test_post_contractor.py
from fastapi.testclient import TestClient
from app.main import create_app


def test_post_contractors_201():
    client = TestClient(create_app())
    resp = client.post(
        "/contractors",
        json={
            "business_name": "ACME",
            "tax_id": "12345678-9",
            "main_contact": "alice@example.com",
            "certifications": ["ISO9001", "OSHA"],
        },
    )
    assert resp.status_code == 201
    body = resp.json()
    assert body["id"] and body["business_name"] == "ACME"
