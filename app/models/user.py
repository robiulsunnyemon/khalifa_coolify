# from sqlalchemy import Column, String, Integer,Boolean,DateTime
# from sqlalchemy.sql import func
# from app.db.db import Base


# class UserModel(Base):
#     __tablename__ = 'users'
#     id = Column(Integer, primary_key=True, index=True)
#     first_name = Column(String,index=True)
#     last_name = Column(String,index=True)
#     email = Column(String,index=True,unique=True)
#     phone_number = Column(String,index=True)
#     district = Column(String,index=True)
#     city = Column(String,index=True)
#     address = Column(String,index=True)
#     password = Column(String)
#     accept_all_terms = Column(Boolean,default=True)
#     is_verified = Column(Boolean)
#     otp = Column(String)
#     role = Column(String,index=True,default="customer")
#     create_time = Column(DateTime,server_default=func.now())
#     update_time = Column(DateTime, server_default=func.now(), onupdate=func.now())


# app/models/user.py
from sqlalchemy import Column, String, Integer, Boolean, DateTime
from sqlalchemy.sql import func
from app.db.db import Base


class UserModel(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, index=True)
    last_name = Column(String, index=True)
    email = Column(String, index=True, unique=True)
    phone_number = Column(String, index=True)
    district = Column(String, index=True)
    city = Column(String, index=True)
    address = Column(String, index=True)
    password = Column(String, nullable=True)  # Google user → password নেই
    accept_all_terms = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    otp = Column(String, nullable=True)  # OTP শুধুমাত্র email ইউজারের জন্য
    role = Column(String, index=True, default="customer")
    profile_image = Column(String, nullable=True)  # Google user profile picture
    auth_provider = Column(String, default="email")  # email / google
    create_time = Column(DateTime, server_default=func.now())
    update_time = Column(DateTime, server_default=func.now(), onupdate=func.now())
