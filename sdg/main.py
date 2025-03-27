from fastapi import FastAPI

from .poc import poc
from .project.router import router as project_router
from .storage.router import router as storage_router
from .data_operator.router import router as operator_router
from .db import init_db

init_db()

app = FastAPI(
    docs_url="/api/docs",
)

app = FastAPI()

app.include_router(project_router)
app.include_router(storage_router)
app.include_router(operator_router)

@app.get("/")
async def hello() -> dict[str, str]:
    return {"message": "Hello World"}

@app.post("/poc")
async def test():
    poc()

if __name__ == '__main__':
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)