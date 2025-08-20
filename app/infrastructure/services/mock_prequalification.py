from fastapi import APIRouter
from pydantic import BaseModel, Field
from typing import List
from app.domain.contractor import PrequalificationStatus
from app.domain.ports import PrequalificationClient

router = APIRouter()


class PrequalificationIn(BaseModel):
    contractorId: str = Field(..., min_length=1)
    certifications: List[str] = []
    yearsOfExperience: int = Field(..., ge=0)


class PrequalificationOut(BaseModel):
    contractorId: str
    status: PrequalificationStatus


@router.post("/external/prequalification", response_model=PrequalificationOut)
def mock_prequalification(req: PrequalificationIn):
    status = _evaluate(req.certifications, req.yearsOfExperience)
    return PrequalificationOut(contractorId=req.contractorId, status=status)


class InProcessPrequalificationClient(PrequalificationClient):
    def evaluate(
        self, *, contractor_id: str, certifications: List[str], years_of_experience: int
    ) -> PrequalificationStatus:
        return _evaluate(certifications, years_of_experience)


def _evaluate(certs: List[str], years: int) -> PrequalificationStatus:
    if len(certs) == 0:
        return PrequalificationStatus.REJECTED
    if len(certs) > 3 and years > 2:
        return PrequalificationStatus.APPROVED
    return PrequalificationStatus.PENDING
