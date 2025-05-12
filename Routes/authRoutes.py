from config.DB import collection
from Models.schema import all_users
from Models.models import User
from controllers.authcontrollers import signup
from fastapi import APIRouter,Body

router = APIRouter()

@router.get("/")
async def getall():
    response = collection.find()
    return all_users(response)

@router.post("/register")
async def register(new_user: User = Body(...)):
    return await signup(new_user)