from config.DB import collection
from Models.models import User
from bson.objectid import ObjectId
from datetime import datetime
from fastapi import HTTPException,Body

async def signup(new_user: User):
    try:
       exist = collection.find_one({"email":new_user.email})
       if exist:
           return HTTPException(status_code=404, detail=f"User already exist")
       
       user_data= new_user.dict()
       user_data["created_at"]=int(datetime.timestamp(datetime.now()))
       user_data["updated_at"]=int(datetime.timestamp(datetime.now()))
      

       response = collection.insert_one(user_data)
         
       return {'status_code':200,"_id":str(response.inserted_id),"message": "User created successfully"}
    except Exception as e:
        return HTTPException({'status_code':500,"detail":f"Some erro occurred, {e}"})