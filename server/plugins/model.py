from dataclasses import dataclass
from typing import List

@dataclass
class DashboardQuery:
    id: str
    title: str
    description: str
    query: str

@dataclass
class QuerySuggestionResponse:
    error: str | None = None
    queries: List[DashboardQuery] | None = None