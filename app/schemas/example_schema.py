from pydantic import BaseModel
from typing import List, Optional

class ExampleSchema(BaseModel):
    id: int
    name: str
    description: Optional[str] = None

class ExampleCreateSchema(BaseModel):
    name: str
    description: Optional[str] = None

class ExampleUpdateSchema(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None

class ExampleResponseSchema(BaseModel):
    id: int
    name: str
    description: Optional[str] = None

    class Config:
        orm_mode = True

class ExampleListResponseSchema(BaseModel):
    examples: List[ExampleResponseSchema]