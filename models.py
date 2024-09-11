from typing import List
from pydantic import BaseModel

class CommandResponse(BaseModel):
    mode: str = "None"
    status: str = "FAILED"
    content: dict[str, str]
    flag: str = ""