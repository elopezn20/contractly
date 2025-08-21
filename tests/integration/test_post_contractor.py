from fastapi.testclient import TestClient
from app.main import create_app


def test_post_contractors_201_and_body_shape():
    client = TestClient(create_app())

    payload = {
        "business_name": "ACME",
        "tax_id": "12345678-9",
        "main_contact": "alice@acme.com",
        "certifications": ["ISO9001", "OSHA"],
        "years_of_experience": 3,
    }

    resp = client.post("/contractors", json=payload)
    assert resp.status_code == 201
    body = resp.json()

    assert set(body.keys()) >= {
        "id",
        "business_name",
        "tax_id",
        "main_contact",
        "certifications",
        "years_of_experience",
    }
    assert body["business_name"] == "ACME"
    assert body["tax_id"] == "12345678-9"
    assert body["certifications"] == ["ISO9001", "OSHA"]
    assert body["years_of_experience"] == 3


def test_post_contractors_400_on_missing_field():
    client = TestClient(create_app())
    bad_payload = {
        # "business_name" missing
        "tax_id": "12345678-9",
        "main_contact": "alice@acme.com",
        "certifications": [],
    }
    resp = client.post("/contractors", json=bad_payload)
    assert resp.status_code == 422
