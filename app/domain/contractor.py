from dataclasses import dataclass
from enum import Enum
from typing import List
from uuid import uuid4


class PrequalificationStatus(str, Enum):
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    PENDING = "PENDING"
    UNASSESSED = "UNASSESSED"


@dataclass(frozen=True)
class Certification:
    code: str


@dataclass
class Contractor:
    id: str
    business_name: str
    tax_id: str
    main_contact: str
    certifications: List[Certification]
    status: PrequalificationStatus

    @staticmethod
    def new(
        business_name: str, tax_id: str, main_contact: str, certs: List[str]
    ) -> "Contractor":
        return Contractor(
            id=str(uuid4()),
            business_name=business_name.strip(),
            tax_id=tax_id.strip(),
            main_contact=main_contact.strip(),
            certifications=[Certification(c) for c in certs or []],
            status=PrequalificationStatus.UNASSESSED,
        )
