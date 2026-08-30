from typing import List, Optional, Literal
from pydantic import BaseModel, Field

class Transaction(BaseModel):
    date: str
    description: str
    amount: float
    running_balance: Optional[float] = None

class ExtractionResult(BaseModel):
    detected_format: Literal["native_text", "image_based"]
    model: str
    document_status: Literal["extracted", "could_not_process"]
    reason: Optional[str] = None
    transactions: List[Transaction] = Field(default_factory=list)
