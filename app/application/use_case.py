from typing import List
from app.domain.contractor import Contractor
from app.domain.ports import ContractorRepository, PrequalificationClient


class CreateContractor:
    def __init__(self, repo: ContractorRepository):
        self.repo = repo

    def execute(
        self,
        *,
        business_name: str,
        tax_id: str,
        main_contact: str,
        certifications: List[str],
    ) -> Contractor:
        if not business_name or not tax_id or not main_contact:
            raise ValueError("business_name, tax_id and main_contact are required")
        contractor = Contractor.new(
            business_name, tax_id, main_contact, certifications or []
        )
        self.repo.add(contractor)
        return contractor


class PrequalifyContractor:
    def __init__(self, repo: ContractorRepository, client: PrequalificationClient):
        self.repo = repo
        self.client = client

    def execute(self, *, contractor_id: str, years_of_experience: int) -> Contractor:
        c = self.repo.get(contractor_id)
        if not c:
            raise ValueError("contractor not found")
        status = self.client.evaluate(
            contractor_id=contractor_id,
            certifications=[cert.code for cert in c.certifications],
            years_of_experience=years_of_experience,
        )
        c.status = status
        self.repo.add(c)
        return c
