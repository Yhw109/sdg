from fastapi import APIRouter
from sqlmodel import func, select
from ..db import SessionDep
from .model import ProjectCreate, ProjectRead, ProjectReadAll, Project

router: APIRouter = APIRouter(
    prefix="/projects",
    tags=["projects"],
)

@router.get("/", response_model=ProjectReadAll)
async def list_projects(session: SessionDep):
    count_statement = select(func.count()).select_from(Project)
    count = session.exec(count_statement).one()
    statement = select(Project).order_by(Project.created_at)    # type: ignore
    projects = session.exec(statement).all()
    return ProjectReadAll(projects=projects, count=count)   # type: ignore

@router.post("/", response_model=ProjectRead)
async def create_project(session: SessionDep, project: ProjectCreate):
    dataset_path = project.raw_dataset_path
    project_db = Project.model_validate(project)
    session.add(project_db)
    session.commit()
    session.refresh(project_db)
    return project
