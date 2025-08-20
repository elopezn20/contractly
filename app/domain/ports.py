from typing import Protocol, List, Optional
from .contractor import Contractor, PrequalificationStatus


class ContractorRepository(Protocol):
    def add(self, c: Contractor) -> None: ...
    def get(self, contractor_id: str) -> Optional[Contractor]: ...
    def list_all(self) -> List[Contractor]: ...


class PrequalificationClient(Protocol):
    def evaluate(
        self, *, contractor_id: str, certifications: List[str], years_of_experience: int
    ) -> PrequalificationStatus: ...
