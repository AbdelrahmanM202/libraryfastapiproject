from fastapi import FastAPI,Depends, Request
from sqlalchemy.orm import Session

from library import models, schemas
from library.database import SessionLocal, engine



models.Base.metadata.create_all(bind=engine)

app = FastAPI()
"""
@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    response = Response("Internal server error", status_code=500)
    try:
        request.state.db = SessionLocal()
        response = await call_next(request)
    finally:
        request.state.db.close()
    return response
"""

@app.get("/")
async def root():
    return {"message":"HelloWorld"}

def get_db(request: Request):
    return request.state.db


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post('/users/', response_model=schemas.UserBase)
def create_users(request: schemas.User, db:Session = Depends(get_db)):
    new_user = models.User(name=request.name,email=request.email,number=request.number)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@app.get('/users/')#, response_model=schemas.UserBase)
def get_users(db:Session = Depends(get_db)):
    users = db.query(models.User).all()
    return users




@app.get('/users/{id}')#, response_model=schemas.UserBase)
def get_user(id:int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPExeption(status_code=status.HTTP_404_NOT_FOUND
                           ,detail=f"Blog with the id {id} is not available")
    return user


@app.post('/users/{id}')#, status_code=status.HTTP_202_ACCEPTED)#, response_model=schemas.UserBase)
def update_user(id:int,request: schemas.User, db: Session = Depends(get_db)):
    db.query(models.User).filter(models.User.id == id).update({'name':'updated name'})
    return 'updated'




    """
    user = db.query(models.User).filter(models.User.id == id).first()
    user = models.User(name=request.name,email=request.email,number=request.number)
    #db.update(user)

    db.commit()
    db.refresh(user)
    if not user:
        raise HTTPExeption(status_code=status.HTTP_404_NOT_FOUND
                           , detail=f"Blog with the id {id} is not available")
                           """
    return user



@app.delete('/users/{id}')
def del_user(id:int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    db.delete(user)
    db.commit()
    db.refresh(user)
    if not user:
        raise HTTPExeption(status_code=status.HTTP_404_NOT_FOUND
                           ,detail=f"Blog with the id {id} is not available")

    return {"message": "Deleted"}



"""
@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.create_user(db, name=user.name,email=user.email,number=user.number)
    if db_user:
        raise HTTPException(status_code=400, detail="Name already registered")
    return crud.create_user(db=db, user=user)
"""