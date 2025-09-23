import os
import uuid
from fastapi import APIRouter, Depends, UploadFile, Form, Request, HTTPException,status
from sqlalchemy.orm import Session
from app.db.db import get_db
from typing import List
from app.models.notification import NotificationModel
from app.schemas.notification import NotificationResponse, NotificationCreate

router = APIRouter(
    prefix="/notifications",
    tags=["Notification"]
)

# Upload directory
UPLOAD_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
    "uploads/notification"
)
os.makedirs(UPLOAD_DIR, exist_ok=True)


# ---------- Create Notification ----------
@router.post("/", response_model=NotificationResponse,status_code=status.HTTP_201_CREATED)
async def create_notification(
    request: Request,
    title: str = Form(...),
    content: str = Form(...),
    image: UploadFile = None,
    db: Session = Depends(get_db)
):
    image_url = None
    if image and image.filename:
        file_ext = image.filename.split(".")[-1]
        unique_filename = f"{uuid.uuid4()}.{file_ext}"
        file_path = os.path.join(UPLOAD_DIR, unique_filename)

        with open(file_path, "wb") as f:
            f.write(await image.read())

        base_url = str(request.base_url)
        image_url = f"{base_url}uploads/notification/{unique_filename}"

    db_notification = NotificationModel(
        title=title,
        content=content,
        image=image_url
    )
    db.add(db_notification)
    db.commit()
    db.refresh(db_notification)
    return db_notification



@router.post("/bulk", response_model=List[NotificationResponse], status_code=status.HTTP_201_CREATED)
async def bulk_notifications(notifications: List[NotificationCreate], db: Session = Depends(get_db)):
    db_notifications = [
        NotificationModel(
            title=notification.title,
            content=notification.content,
            image=notification.image
        ) for notification in notifications
    ]

    db.add_all(db_notifications)  # Add all at once
    db.commit()                  # Single commit
    for notif in db_notifications:
        db.refresh(notif)        # Refresh objects to get IDs

    return db_notifications






# ---------- Get All Notifications ----------
@router.get("/", response_model=List[NotificationResponse],status_code=status.HTTP_200_OK)
async def get_all_notifications(db: Session = Depends(get_db)):
    notifications = db.query(NotificationModel).order_by(NotificationModel.created_at.desc()).all()
    return notifications


# ---------- Get Single Notification ----------
@router.get("/{notification_id}", response_model=NotificationResponse,status_code=status.HTTP_200_OK)
async def get_notification(notification_id: int, db: Session = Depends(get_db)):
    notification = db.query(NotificationModel).filter(NotificationModel.id == notification_id).first()
    if not notification:
        raise HTTPException(status_code=404, detail="Notification not found")
    return notification



# ---------- Delete Notification ----------
@router.delete("/{notification_id}",status_code=status.HTTP_204_NO_CONTENT)
async def delete_notification(notification_id: int, db: Session = Depends(get_db)):
    notification = db.query(NotificationModel).filter(NotificationModel.id == notification_id).first()
    if not notification:
        raise HTTPException(status_code=404, detail="Notification not found")

    db.delete(notification)
    db.commit()
    return {"message": "Notification deleted successfully"}
