from sqlalchemy.orm import Session
from app.models import User


def get_user_by_id(db: Session, user_id: int) -> User | None:
    """ID로 사용자 조회"""
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_email(db: Session, email: str) -> User | None:
    """이메일로 사용자 조회"""
    return db.query(User).filter(User.email == email).first()


def get_user_by_username(db: Session, username: str) -> User | None:
    """사용자명으로 사용자 조회"""
    return db.query(User).filter(User.username == username).first()


def create_user(db: Session, user_create_data: dict, hashed_password: str) -> User:
    """새 사용자 생성

    Args:
        db: 데이터베이스 세션
        user_create_data: username, email을 포함하는 딕셔너리 또는 Pydantic 모델
        hashed_password: 해시된 비밀번호

    Returns:
        생성된 User 객체
    """
    # Pydantic 모델인 경우 dict로 변환
    if hasattr(user_create_data, 'model_dump'):
        data = user_create_data.model_dump(exclude={'password'})
    elif hasattr(user_create_data, 'dict'):
        data = user_create_data.dict(exclude={'password'})
    else:
        data = dict(user_create_data)
        data.pop('password', None)

    db_user = User(
        username=data['username'],
        email=data['email'],
        hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
