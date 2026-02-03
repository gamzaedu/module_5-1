from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.user import UserCreate, UserResponse
from app.schemas.auth import UserLogin, Token
from app.crud.user import get_user_by_email, get_user_by_username, create_user
from app.utils.auth import (
    get_password_hash,
    verify_password,
    create_access_token,
    get_current_user,
)

router = APIRouter()


@router.post("/signup", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def signup(user: UserCreate, db: Session = Depends(get_db)):
    """회원가입 엔드포인트

    Args:
        user: 회원가입 정보 (username, email, password)
        db: 데이터베이스 세션

    Returns:
        생성된 사용자 정보 (password 제외)

    Raises:
        HTTPException 400: 이메일 또는 username이 이미 존재하는 경우
    """
    # 이메일 중복 체크
    if get_user_by_email(db, user.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    # username 중복 체크
    if get_user_by_username(db, user.username):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already taken"
        )

    # 비밀번호 해싱 후 사용자 생성
    hashed_password = get_password_hash(user.password)
    db_user = create_user(db, user, hashed_password)

    return db_user


@router.post("/login", response_model=Token)
def login(user_login: UserLogin, db: Session = Depends(get_db)):
    """로그인 엔드포인트

    Args:
        user_login: 로그인 정보 (email, password)
        db: 데이터베이스 세션

    Returns:
        JWT 액세스 토큰

    Raises:
        HTTPException 401: 이메일 또는 비밀번호가 올바르지 않은 경우
    """
    # 이메일로 사용자 조회
    user = get_user_by_email(db, user_login.email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # 비밀번호 검증
    if not verify_password(user_login.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # JWT 토큰 생성
    access_token = create_access_token(data={"sub": user.username})

    return Token(access_token=access_token, token_type="bearer")


@router.get("/me", response_model=UserResponse)
async def get_me(current_user=Depends(get_current_user)):
    """현재 로그인한 사용자 정보 조회

    Args:
        current_user: 현재 인증된 사용자 (get_current_user 의존성)

    Returns:
        현재 사용자 정보
    """
    return current_user
