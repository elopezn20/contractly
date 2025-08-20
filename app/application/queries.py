from typing import List
from app.domain.contractor import Contractor
from app.domain.ports import ContractorRepository


class ListContractors:
    def __init__(self, repo: ContractorRepository):
        self.repo = repo

    def execute(self) -> List[Contractor]:
        return self.repo.list_all()
