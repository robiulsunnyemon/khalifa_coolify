from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.routers.food_category import router as food_category_router
from app.routers.user import router as user_router
from app.db.db import Base, engine
from app.routers.food import router as food_router
from app.routers.cart import router as cart_router
from app.routers.food_rating import router as food_rating_router
from app.routers.order import router as order_router
from app.routers.search import router as search_router
from app.payment.bkash.payment_routers import router as payment_routers
from app.routers.notification import router as notification_router
from app.routers.payment_history import router as payment_history_router
from fastapi.middleware.cors import CORSMiddleware
from app.routers.user_me import router as user_me_router
from app.routers.variation_of_food import router as variation_of_food_router
from app.routers.menu import router as menu_router

app = FastAPI(title="Alkhalifa backend update")

# Base.metadata.drop_all(bind=engine)

Base.metadata.create_all(bind=engine)

app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")


origins = [
    "http://localhost",
    "http://localhost:8000",
    "https://your-frontend-domain.com"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)





@app.get("/",tags=["Root"])
async def root():
    return {"message": "Hello Alkhalifa's Employee"}

# Routers
app.include_router(user_router)
app.include_router(food_category_router)
app.include_router(cart_router)
app.include_router(food_rating_router)
app.include_router(order_router)
app.include_router(search_router)
app.include_router(payment_routers)
app.include_router(food_router)
app.include_router(notification_router)
app.include_router(payment_history_router)
app.include_router(user_me_router)
app.include_router(variation_of_food_router)
app.include_router(menu_router)