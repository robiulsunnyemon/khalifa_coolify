from fastapi import APIRouter, Depends, HTTPException,status
from app.schemas.user import UserCreate, UserRead, UserOTPVerify, ResendOTP, ResetPassword, LoginUserModel, UserUpdate
from app.db.db import get_db
from app.models.user import UserModel
from sqlalchemy.orm import Session
from app.utils.user_info import get_user_info


router = APIRouter(prefix="/profile", tags=["Profile"])


@router.get("/me",response_model=UserRead ,status_code=status.HTTP_200_OK)
async def read_user_by_token(db: Session = Depends(get_db),user: dict = Depends(get_user_info)):
    user_id = user["user_id"]
    db_user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if db_user is None :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="User not found")
    return db_user



@router.put("/update}", response_model=UserRead,status_code=status.HTTP_201_CREATED)
def update_user(user: UserUpdate,user_info: dict = Depends(get_user_info), db: Session = Depends(get_db)):
    user_id = user_info["user_id"]
    db_user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    for key, value in user.model_dump(exclude_unset=True).items():
        setattr(db_user, key, value)
    db.commit()
    db.refresh(db_user)
    return db_user

