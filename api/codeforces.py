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


@router.get('/{user_name}', response_model=schemas.CodeforcesStatistics, summary='获取 Codeforces 用户统计数据')
async def get_codeforces_statistics(user_name: str, db: Session = Depends(get_db)):
    db_codeforces_statistics = crud.get_codeforces_statistics(db, user_name)
    if db_codeforces_statistics is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='用户不存在')
    codeforces_statistics = schemas.CodeforcesStatistics.from_orm(db_codeforces_statistics)
    print(codeforces_statistics)
    return codeforces_statistics
