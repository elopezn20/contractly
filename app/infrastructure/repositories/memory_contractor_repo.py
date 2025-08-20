from typing import List, Optional
from app.domain.contractor import Contractor
from app.domain.ports import ContractorRepository


class InMemoryContractorRepo(ContractorRepository):
    def __init__(self):
        self._items: dict[str, Contractor] = {}

    def add(self, c: Contractor) -> None:
        self._items[c.id] = c

    def get(self, contractor_id: str) -> Optional[Contractor]:
        return self._items.get(contractor_id)

    def list_all(self) -> List[Contractor]:
        return list(self._items.values())
