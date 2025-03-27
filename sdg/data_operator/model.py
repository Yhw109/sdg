from pydantic import BaseModel

class Operator(BaseModel):
    name: str
    description: str