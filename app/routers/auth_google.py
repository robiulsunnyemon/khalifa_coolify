# app/routers/auth_google.py
from fastapi import APIRouter, Depends, Request,HTTPException,status
import requests
from sqlalchemy.orm import Session
from app.db.db import get_db
from app.models.user import UserModel
from app.utils.token_generation import create_access_token

router = APIRouter(prefix="/auth/google", tags=["Google Auth"])



@router.post("/token",status_code=status.HTTP_201_CREATED)
async def google_login_token(access_token: str, db: Session = Depends(get_db)):

    response = requests.get(
        f'https://www.googleapis.com/oauth2/v2/userinfo?access_token={access_token}'
    )
    if response.status_code != 200:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid Google token")

    user_info = response.json()
    email = user_info["email"]
    name = user_info.get("name", "")
    picture = user_info.get("picture", "")

    # 2️⃣ Check DB
    db_user = db.query(UserModel).filter(UserModel.email == email).first()
    if not db_user:
        # Create new Google user
        db_user = UserModel(
            first_name=name.split(" ")[0] if name else "",
            last_name=" ".join(name.split(" ")[1:]) if len(name.split(" ")) > 1 else "",
            email=email,
            phone_number="",
            district="",
            city="",
            address="",
            password=None,  # Google user → password নেই
            is_verified=True,
            role="customer",
            profile_image=picture,
            auth_provider="google",
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)

    # 3️⃣ Generate JWT token
    jwt_token = create_access_token(
        data={"sub": db_user.email, "user_id": db_user.id, "role": db_user.role}
    )

    return {"access_token": jwt_token, "token_type": "bearer"}