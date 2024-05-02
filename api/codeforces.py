from fastapi import APIRouter, Depends, status, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session

from dao import crud, schemas
from dao.database import SessionLocal
from crawl import main as crawl_main


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


router = APIRouter(
    prefix='/codeforces',
    tags=['codeforces']
)


@router.get('', response_model=schemas.RecentContests, summary='获取 Codeforces 用户统计数据')
async def get_codeforces_stastics(db: Session = Depends(get_db)):
    ...
