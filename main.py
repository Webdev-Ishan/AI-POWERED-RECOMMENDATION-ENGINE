from fastapi import FastAPI,HTTPException,Body,APIRouter
from Routes.authRoutes import router

app= FastAPI()







app.include_router(router)
