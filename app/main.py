from fastapi import FastAPI
from app.application.use_case import (
    CreateContractor,
    PrequalifyContractor,
)
from app.application.queries import ListContractors
from app.infrastructure.repositories.memory_contractor_repo import (
    InMemoryContractorRepo,
)
from app.infrastructure.services.mock_prequalification import (
    router as mock_router,
    InProcessPrequalificationClient,
)
from app.infrastructure.web.api import make_router


def create_app() -> FastAPI:
    app = FastAPI(title="Contractly MVP")

    repo = InMemoryContractorRepo()
    create_uc = CreateContractor(repo)
    list_uc = ListContractors(repo)
    preq_client = InProcessPrequalificationClient()
    preq_uc = PrequalifyContractor(repo, preq_client)

    app.include_router(make_router(create_uc, list_uc, preq_uc))
    app.include_router(mock_router)
    return app


app = create_app()
