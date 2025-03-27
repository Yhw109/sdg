from fastapi import APIRouter

from sdg.data_operator.model import Operator

from .operator import OperatorMeta

router = APIRouter(
    prefix="/operators",
    tags=["operators"]
)

@router.get("/")
async def read_operators():
    regisery = OperatorMeta.get_registry()
    print(regisery.keys())
    return str(regisery.keys())