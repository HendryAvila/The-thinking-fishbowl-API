from email.mime import base
from fastapi import FastAPI
from sql_app.database import engine,  get_db
from sql_app import models
from app.routers import books, users, author, gender, auth
from fastapi.middleware.cors import CORSMiddleware




app = FastAPI(
    prefix="/the-fishbowl",
    title="The thinking fishbowl",
)

app.include_router(books.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(author.router)
app.include_router(gender.router)

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    
)



#models.Base.metadata.create_all(engine)
get_db()

@app.get("/")
async def  root():
    return {"message": "Welcome to The thinking fishbowl!!"}


'''
#source venv/scripts/activate
#uvicorn app.main:app --reload
#http://127.0.0.1:8000
'''

