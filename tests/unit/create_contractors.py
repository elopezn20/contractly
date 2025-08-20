# tests/unit/test_create_contractor.py
from app.application.use_case import CreateContractor
from app.infrastructure.repositories.memory_contractor_repo import (
    InMemoryContractorRepo,
)


def test_create_contractor_happy_path():
    uc = CreateContractor(InMemoryContractorRepo())
    c = uc.execute(
        business_name="ACME",
        tax_id="123",
        main_contact="alice",
        certifications=["ISO9001"],
    )
    assert c.id and c.business_name == "ACME"
