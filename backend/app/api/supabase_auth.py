from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel, EmailStr
from typing import Optional

from app.services.supabase_user_service import SupabaseUserService
from app.core.security import create_access_token, verify_token
from app.core.config import settings

router = APIRouter()

# OAuth2密码流
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/supabase-auth/login")

# 初始化服务
user_service = SupabaseUserService()

# Pydantic模型
class UserResponse(BaseModel):
    id: int
    email: str
    name: str
    role: str
    training_status: str
    training_progress: int
    is_active: bool

class Token(BaseModel):
    access_token: str
    token_type: str
    user: UserResponse

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class RegisterRequest(BaseModel):
    email: EmailStr
    password: str
    name: str
    role: str = "teacher"  # 默认为教师角色

class UpdateProfileRequest(BaseModel):
    name: Optional[str] = None
    training_status: Optional[str] = None
    training_progress: Optional[int] = None

async def get_current_user(token: str = Depends(oauth2_scheme)):
    """获取当前用户"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="无法验证凭据",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = verify_token(token)
        user_id: int = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except Exception:
        raise credentials_exception
    
    user = await user_service.get_user_by_id(user_id)
    if user is None:
        raise credentials_exception
    
    return user

@router.post("/register", response_model=UserResponse)
async def register(register_data: RegisterRequest):
    """用户注册"""
    try:
        # 检查邮箱是否已存在
        existing_user = await user_service.get_user_by_email(register_data.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="邮箱已被注册"
            )
        
        # 验证角色
        if register_data.role not in ["teacher", "manager"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="无效的用户角色"
            )
        
        # 创建用户
        user_data = {
            "email": register_data.email,
            "name": register_data.name,
            "role": register_data.role,
            "training_status": "not_started",
            "training_progress": 0,
            "is_active": True
        }
        
        user = await user_service.create_user(user_data, register_data.password)
        
        return UserResponse(
            id=user["id"],
            email=user["email"],
            name=user["name"],
            role=user["role"],
            training_status=user["training_status"],
            training_progress=user["training_progress"],
            is_active=user["is_active"]
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"注册失败: {str(e)}"
        )

@router.post("/login", response_model=Token)
async def login(login_data: LoginRequest):
    """用户登录"""
    try:
        # 验证用户
        user = await user_service.authenticate_user(login_data.email, login_data.password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="邮箱或密码错误",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # 检查用户是否激活
        if not user.get("is_active", True):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="账户已被停用",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # 创建访问令牌
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": str(user["id"])}, expires_delta=access_token_expires
        )
        
        user_response = UserResponse(
            id=user["id"],
            email=user["email"],
            name=user["name"],
            role=user["role"],
            training_status=user["training_status"],
            training_progress=user["training_progress"],
            is_active=user["is_active"]
        )
        
        return Token(
            access_token=access_token,
            token_type="bearer",
            user=user_response
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"登录失败: {str(e)}"
        )

@router.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user: dict = Depends(get_current_user)):
    """获取当前用户信息"""
    return UserResponse(
        id=current_user["id"],
        email=current_user["email"],
        name=current_user["name"],
        role=current_user["role"],
        training_status=current_user["training_status"],
        training_progress=current_user["training_progress"],
        is_active=current_user["is_active"]
    )

@router.put("/profile", response_model=UserResponse)
async def update_profile(
    update_data: UpdateProfileRequest,
    current_user: dict = Depends(get_current_user)
):
    """更新用户资料"""
    try:
        # 准备更新数据
        update_dict = {}
        if update_data.name is not None:
            update_dict["name"] = update_data.name
        if update_data.training_status is not None:
            update_dict["training_status"] = update_data.training_status
        if update_data.training_progress is not None:
            update_dict["training_progress"] = update_data.training_progress
        
        if not update_dict:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="没有提供更新数据"
            )
        
        # 更新用户信息
        success = await user_service.update_user(current_user["id"], update_dict)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="更新用户信息失败"
            )
        
        # 获取更新后的用户信息
        updated_user = await user_service.get_user_by_id(current_user["id"])
        
        return UserResponse(
            id=updated_user["id"],
            email=updated_user["email"],
            name=updated_user["name"],
            role=updated_user["role"],
            training_status=updated_user["training_status"],
            training_progress=updated_user["training_progress"],
            is_active=updated_user["is_active"]
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"更新资料失败: {str(e)}"
        )

@router.post("/logout")
async def logout():
    """用户登出"""
    # 在实际应用中，可以在这里处理令牌黑名单等逻辑
    return {"message": "登出成功"}

# 管理员专用路由
@router.get("/users", response_model=list[UserResponse])
async def get_all_users(current_user: dict = Depends(get_current_user)):
    """获取所有用户（管理员功能）"""
    if current_user["role"] != "manager":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="权限不足"
        )
    
    try:
        users = await user_service.get_all_users()
        return [
            UserResponse(
                id=user["id"],
                email=user["email"],
                name=user["name"],
                role=user["role"],
                training_status=user["training_status"],
                training_progress=user["training_progress"],
                is_active=user["is_active"]
            )
            for user in users
        ]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"获取用户列表失败: {str(e)}"
        )

@router.put("/users/{user_id}/deactivate")
async def deactivate_user(user_id: int, current_user: dict = Depends(get_current_user)):
    """停用用户（管理员功能）"""
    if current_user["role"] != "manager":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="权限不足"
        )
    
    try:
        success = await user_service.deactivate_user(user_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="用户不存在"
            )
        
        return {"message": "用户已停用"}
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"停用用户失败: {str(e)}"
        )