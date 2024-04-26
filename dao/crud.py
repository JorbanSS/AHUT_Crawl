from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import and_

from . import models, schemas


def get_recent_contests(db: Session):
    return db.query(models.RecentContests).all()


def clear_recent_contests(db: Session):
    db.query(models.RecentContests).delete()
    db.commit()


def get_user_by_uid(db: Session, UID: str):
    return db.query(models.User).filter(models.User.UID == UID).first()


def get_rating_by_uid(db: Session, UID: str):
    return db.query(models.Rating).filter(models.Rating.UID == UID).first()


def add_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)


def bind_user_account(db: Session, rating: models.Rating, user_bind: schemas.UserBind):
    if rating is not None:
        if user_bind.CodeforcesID is not None:
            rating.CodeforcesID = user_bind.CodeforcesID
        if user_bind.NowcoderID is not None:
            rating.NowcoderID = user_bind.NowcoderID
        if user_bind.AtcoderID is not None:
            rating.AtcoderID = user_bind.AtcoderID
    else:
        new_data = models.Rating(
            UID=user_bind.UID,
        )
        if user_bind.CodeforcesID is not None:
            new_data.CodeforcesID = user_bind.CodeforcesID
        if user_bind.NowcoderID is not None:
            new_data.NowcoderID = user_bind.NowcoderID
        if user_bind.AtcoderID is not None:
            new_data.AtcoderID = user_bind.AtcoderID
        db.add(new_data)
    db.commit()


def get_user_name_list_by_account(db: Session, account_name: str):
    return (
        db.query(getattr(models.Rating, account_name))
        .filter(and_(
            getattr(models.Rating, account_name).is_not(None),
            getattr(models.Rating, account_name) != ''
        ))
        .all()
    )


def get_rating_rank(db: Session):
    db_rating_rank = (
        db.query(models.Rating, models.User.UserName)
        .join(models.User, models.Rating.UID == models.User.UID)
        .all()
    )
    rating_rank = []
    for item, user_name in db_rating_rank:
        item.CodeforcesID = item.CodeforcesID if item.CodeforcesID is not None else ''
        item.NowcoderID = item.NowcoderID if item.NowcoderID is not None else ''
        item.AtcoderID = item.AtcoderID if item.AtcoderID is not None else ''
        item.UserName = user_name if user_name is not None else ''
        rating_rank.append(item)
    return rating_rank


def clear_rating_rank(db: Session):
    db.query(models.Rating).delete()
    db.commit()
