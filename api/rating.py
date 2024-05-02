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
    ret = {
        'RatingRank': db_rating_rank_list,
        'Count': len(db_rating_rank_list)
    }
    return ret


@router.put('', response_model=schemas.BaseResponse, summary='拉取用户评分')
async def scrape_rating(background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    db_codeforces_user_list = crud.get_user_name_list_by_account(db, 'CodeforcesID')
    codeforces_user_list = [user.CodeforcesID for user in db_codeforces_user_list]
    codeforces_user_list_str = ';'.join(codeforces_user_list)
    kwargs = {'user_name_list': codeforces_user_list_str}
    background_tasks.add_task(crawl_main.get_codeforces_rating, **kwargs)

    db_atcoder_user_list = crud.get_user_name_list_by_account(db, 'AtcoderID')
    for user in db_atcoder_user_list:
        kwargs = {'user_name': user.AtcoderID}
        background_tasks.add_task(crawl_main.get_atcoder_rating, **kwargs)

    db_nowcoder_user_list = crud.get_user_name_list_by_account(db, 'NowcoderID')
    for user in db_nowcoder_user_list:
        kwargs = {'ncid': user.NowcoderID}
        background_tasks.add_task(crawl_main.get_nowcoder_rating, **kwargs)
    return {}
