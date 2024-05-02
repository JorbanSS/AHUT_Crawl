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
    prefix='/recentcontests',
    tags=['recent contests']
)


@router.get('', response_model=schemas.RecentContests, summary='获取近期比赛')
async def get_recent_contests(db: Session = Depends(get_db)):
    recent_contests_orm_obj = crud.get_recent_contests(db)
    db_recent_contests = [schemas.RecentContest.from_orm(contest).dict() for contest in recent_contests_orm_obj]
    ret = {
        'RecentContests': db_recent_contests,
        'Count': len(db_recent_contests)
    }
    return ret


@router.put('', response_model=schemas.BaseResponse, summary='拉取近期比赛')
async def scrape_recent_contests(background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    crud.clear_recent_contests(db)
    background_tasks.add_task(crawl_main.get_codeforces_contests)
    background_tasks.add_task(crawl_main.get_nowcoder_contests)
    background_tasks.add_task(crawl_main.get_atcoder_contests)
    background_tasks.add_task(crawl_main.get_luogu_contests)
    return {}
