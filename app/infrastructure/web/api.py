from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import List, Dict
from app.application.use_case import (
    CreateContractor,
    PrequalifyContractor,
)
from app.application.queries import ListContractors
from app.domain.contractor import PrequalificationStatus

router = APIRouter()


class CreateContractorBody(BaseModel):
    business_name: str = Field(..., min_length=1)
    tax_id: str = Field(..., min_length=1)
    main_contact: str = Field(..., min_length=1)
    certifications: List[str] = []
    years_of_experience: int = Field(..., ge=0)


class ContractorOut(BaseModel):
    id: str
    business_name: str
    tax_id: str
    main_contact: str
    certifications: List[str]
    status: PrequalificationStatus


def make_router(
    create_uc: CreateContractor,
    list_uc: ListContractors,
    prequalify_uc: PrequalifyContractor,
) -> APIRouter:
    @router.post("/contractors", response_model=ContractorOut, status_code=201)
    def create_contractor(body: CreateContractorBody):
        try:
            c = create_uc.execute(
                business_name=body.business_name,
                tax_id=body.tax_id,
                main_contact=body.main_contact,
                certifications=body.certifications,
                years_of_experience=body.years_of_experience,
            )
            return ContractorOut(
                id=c.id,
                business_name=c.business_name,
                tax_id=c.tax_id,
                main_contact=c.main_contact,
                certifications=[cert.code for cert in c.certifications],
                status=c.status,
            )
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))

    @router.get("/contractors", response_model=List[ContractorOut], status_code=200)
    def list_contractors():
        items = list_uc.execute()
        return [
            ContractorOut(
                id=c.id,
                business_name=c.business_name,
                tax_id=c.tax_id,
                main_contact=c.main_contact,
                certifications=[cert.code for cert in c.certifications],
                status=c.status,
            )
            for c in items
        ]

    @router.post(
        "/contractors/{contractor_id}/prequalify",
        response_model=ContractorOut,
        status_code=200,
    )
    def prequalify(contractor_id: str):
        try:
            c = prequalify_uc.execute(contractor_id=contractor_id)
            return ContractorOut(
                id=c.id,
                business_name=c.business_name,
                tax_id=c.tax_id,
                main_contact=c.main_contact,
                certifications=[cert.code for cert in c.certifications],
                status=c.status,
            )
        except ValueError as e:
            raise HTTPException(status_code=404, detail=str(e))

    @router.get("/bff/contractors/summary", status_code=200)
    def contractors_summary() -> Dict[str, int]:
        items = list_uc.execute()
        total = len(items)
        counts = {
            "APPROVED": 0,
            "REJECTED": 0,
            "PENDING": 0,
            "UNASSESSED": 0,
        }
        for c in items:
            counts[c.status.value] += 1
        return {
            "total_registered": total,
            "approved": counts["APPROVED"],
            "rejected": counts["REJECTED"],
            "pending": counts["PENDING"],
            "unassessed": counts["UNASSESSED"],
        }

    return router
