from app.application.use_case import CreateContractor
from app.infrastructure.repositories.memory_contractor_repo import (
    InMemoryContractorRepo,
)


def test_create_contractor_happy_path():
    repo = InMemoryContractorRepo()
    uc = CreateContractor(repo)

    c = uc.execute(
        business_name="ACME",
        tax_id="12345678-9",
        main_contact="alice@acme.com",
        certifications=["ISO9001", "OSHA"],
        years_of_experience=3,
    )

    assert c.id
    assert c.business_name == "ACME"
    assert c.tax_id == "12345678-9"
    assert [x.code for x in c.certifications] == ["ISO9001", "OSHA"]
    assert c.years_of_experience == 3


def test_create_contractor_validation_error():
    repo = InMemoryContractorRepo()
    uc = CreateContractor(repo)

    try:
        uc.execute(
            business_name="",
            tax_id="123",
            main_contact="a@a.com",
            certifications=[],
            years_of_experience=3,
        )
        assert False, "Expected ValueError for empty business_name"
    except ValueError as e:
        assert "business_name" in str(e)
