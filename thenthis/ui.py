from typing import Optional
from pydantic import BaseModel


class Pivot(BaseModel):
    name: str
    host: str
    port: Optional[int] = 8000
    doc: Optional[str] = None
