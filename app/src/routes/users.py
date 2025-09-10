from fastapi import APIRouter, HTTPException
from typing import List
from datetime import datetime
from models.models import User, UserCreate, UserRole
from utils.logger import get_logger


router = APIRouter()
logger = get_logger(__name__)

fake_users_db = []
current_id = 1

def get_next_id():
    global current_id
    next_id = current_id
    current_id += 1
    return next_id

@router.post("/users/", response_model=User)
async def create_user(user: UserCreate):
    logger.info("Creating new user", extra={"user_email": user.email, "username": user.username})
    
    
    for existing_user in fake_users_db:
        if existing_user["email"] == user.email:
            logger.warning("User creation failed: email already exists", extra={"user_email": user.email})
            raise HTTPException(status_code=400, detail="Email already registered")
    
    db_user = {
        "id": get_next_id(),
        "username": user.username,
        "email": user.email,
        "full_name": user.full_name,
        "role": UserRole.USER,
        "is_active": True,
        "created_at": datetime.now(),
        "hashed_password": f"fakehashed{user.password}" 
    }
    fake_users_db.append(db_user)
    
    logger.info("User created successfully", extra={"user_id": db_user["id"]})
    return db_user

@router.get("/users/", response_model=List[User])
async def read_users(skip: int = 0, limit: int = 10):
    logger.info("Fetching list of users", extra={"skip": skip, "limit": limit})
    return fake_users_db[skip : skip + limit]

@router.get("/users/{user_id}", response_model=User)
async def read_user(user_id: int):
    logger.info("Fetching user by ID", extra={"user_id": user_id})
    for user in fake_users_db:
        if user["id"] == user_id:
            return user
    logger.warning("User not found", extra={"user_id": user_id})
    raise HTTPException(status_code=404, detail="User not found")

@router.delete("/users/{user_id}")
async def delete_user(user_id: int):
    logger.info("Attempting to delete user", extra={"user_id": user_id})
    for index, user in enumerate(fake_users_db):
        if user["id"] == user_id:
            deleted_user = fake_users_db.pop(index)
            logger.info("User deleted successfully", extra={"user_id": user_id})
            return {"message": "User deleted successfully"}
    
    logger.warning("Delete failed: user not found", extra={"user_id": user_id})
    raise HTTPException(status_code=404, detail="User not found")