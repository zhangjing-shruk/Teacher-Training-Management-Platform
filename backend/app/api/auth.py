from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr

from app.core.database import get_db
from app.core.security import verify_password, create_access_token, verify_token, get_password_hash
from app.models.user import User, UserRole, TrainingStatus
from app.core.config import settings

router = APIRouter()

# OAuth2密码流
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/login")


# Pydantic模型
class UserResponse(BaseModel):
    id: int
    email: str
    name: str
    role: str
    training_status: str
    training_progress: int

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str
    user: UserResponse


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class ResetPasswordRequest(BaseModel):
    email: EmailStr
    newPassword: str


def get_user_by_email(db: Session, email: str):
    """根据邮箱获取用户"""
    return db.query(User).filter(User.email == email).first()


def authenticate_user(db: Session, email: str, password: str):
    """验证用户"""
    user = get_user_by_email(db, email)
    if not user or not verify_password(password, user.hashed_password):
        return False
    return user


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """获取当前用户"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="无法验证凭据",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = verify_token(token)
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except Exception:
        raise credentials_exception
    
    user = get_user_by_email(db, email=email)
    if user is None:
        raise credentials_exception
    return user


@router.post("/login", response_model=Token)
async def login(login_data: LoginRequest, db: Session = Depends(get_db)):
    """用户登录"""
    # 添加调试日志
    print(f"DEBUG: 登录请求 - Email: {login_data.email}, Password: {login_data.password[:3]}***")
    
    user = authenticate_user(db, login_data.email, login_data.password)
    if not user:
        print(f"DEBUG: 认证失败 - Email: {login_data.email}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="邮箱或密码错误",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    print(f"DEBUG: 认证成功 - User: {user.email}, Role: {user.role}")
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    
    user_response = UserResponse(
        id=user.id,
        email=user.email,
        name=user.name,
        role=user.role.value,
        training_status=user.training_status.value,
        training_progress=user.training_progress
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": user_response
    }


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user: User = Depends(get_current_user)):
    """获取当前用户信息"""
    return UserResponse(
        id=current_user.id,
        email=current_user.email,
        name=current_user.name,
        role=current_user.role.value,
        training_status=current_user.training_status.value,
        training_progress=current_user.training_progress
    )


@router.post("/logout")
async def logout():
    """登出"""
    return {"message": "登出成功"}


@router.post("/reset-password")
async def reset_password(reset_data: ResetPasswordRequest, db: Session = Depends(get_db)):
    """重置密码"""
    # 查找用户
    user = get_user_by_email(db, reset_data.email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="用户不存在"
        )
    
    # 验证新密码长度
    if len(reset_data.newPassword) < 6:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="密码长度至少为6位"
        )
    
    try:
        # 更新密码
        user.hashed_password = get_password_hash(reset_data.newPassword)
        db.commit()
        
        return {"message": "密码重置成功"}
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="重置密码失败，请重试"
        )