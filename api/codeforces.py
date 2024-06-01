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


@router.get('/{user_name}', response_model=schemas.CodeforcesStatistics | schemas.BaseResponse, summary='获取 Codeforces 用户统计数据')
async def get_codeforces_statistics(user_name: str, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    if crud.get_rating_by_codeforces_user_name(db, user_name) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='用户不存在')
    db_codeforces_statistics = crud.get_codeforces_statistics(db, user_name)
    if db_codeforces_statistics is None:
        background_tasks.add_task(crawl_main.get_codeforces_user_statistics, user_name)
        return {
            'Code': 0,
            'Msg': '正在获取用户数据'
        }
    codeforces_statistics = schemas.CodeforcesStatistics.from_orm(db_codeforces_statistics)
    return {
        **codeforces_statistics.dict(),
        'Msg': 'OK'
    }
