from fastapi import APIRouter, Depends, status, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session

from dao import crud, schemas
from dao.database import SessionLocal, engine
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
    prefix='/rating',
    tags=['rating']
)


@router.get('', response_model=schemas.RatingRank, summary='获取用户评分排行榜')
async def get_rating_rank(db: Session = Depends(get_db)):
    db_rating_rank_orm_obj = crud.get_rating_rank(db)
    db_rating_rank_list = [schemas.RatingBase.from_orm(rating).dict() for rating in db_rating_rank_orm_obj]
    print(db_rating_rank_list)
    ret = {
        'RatingRank': db_rating_rank_list,
        'Count': len(db_rating_rank_list)
    }
    return ret


@router.put('', response_model=schemas.BaseResponse, summary='拉取用户评分')
async def scrape_rating(background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    db_user_list = crud.get_uid_list_by_account(db, 'CodeforcesID')
    codeforces_id_list = [user.CodeforcesID for user in db_user_list]
    codeforces_id_list_str = ';'.join(codeforces_id_list)
    print(codeforces_id_list_str)
    background_tasks.add_task(crawl_main.get_codeforces_rating(codeforces_id_list_str))
    return {}
