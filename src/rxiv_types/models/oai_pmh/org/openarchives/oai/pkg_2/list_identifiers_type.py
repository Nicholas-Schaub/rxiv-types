from dataclasses import field
from pydantic.dataclasses import dataclass
from typing import List, Optional
from .header_type import HeaderType
from .resumption_token_type import ResumptionTokenType

__NAMESPACE__ = "http://www.openarchives.org/OAI/2.0/"


@dataclass
class ListIdentifiersType:
    header: List[HeaderType] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://www.openarchives.org/OAI/2.0/",
            "min_occurs": 1,
        }
    )
    resumption_token: Optional[ResumptionTokenType] = field(
        default=None,
        metadata={
            "name": "resumptionToken",
            "type": "Element",
            "namespace": "http://www.openarchives.org/OAI/2.0/",
        }
    )
