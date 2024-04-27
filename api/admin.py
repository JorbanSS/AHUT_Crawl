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
    prefix='/admin',
    tags=['admin']
)


@router.post('/user', response_model=schemas.BaseResponse, summary='新增用户')
async def add_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_uid(db, user.UID)
    if db_user is not None:
        return {
            'Code': status.HTTP_409_CONFLICT,
            'Msg': f'UID 为 {user.UID} 的用户已存在，用户名为 {db_user.UserName}'
        }
    crud.add_user(db, user)
    return {}


@router.post('/user/bind', response_model=schemas.BaseResponse, summary='绑定用户账号')
async def bind_user_account(user_bind: schemas.UserBind, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_uid(db, user_bind.UID)
    if db_user is None:
        return {
            'Code': status.HTTP_404_NOT_FOUND,
            'Msg': f'UID 为 {user_bind.UID} 的用户不存在'
        }
    db_rating = crud.get_rating_by_uid(db, user_bind.UID)
    if user_bind.NowcoderID is not None:
        background_tasks.add_task(crawl_main.get_nowcoder_id, user_name=user_bind.NowcoderID, uid=user_bind.UID)
        user_bind.NowcoderID = None
    crud.bind_user_account(db, db_rating, user_bind)
    return {}
