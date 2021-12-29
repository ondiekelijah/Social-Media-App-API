from fastapi import APIRouter,Depends,status,HTTPException,Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from .. import database,schemas,models,utils,oath2


router = APIRouter(tags=['Authentication'])

@router.post('/login', response_model=schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db )):

    # OAuth2PasswordRequestForm returns
    
    # {
    #     "username": "",
    #     "password" : ""
    # }


    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Invalid credentials",
        )

    if not utils.verify(user_credentials.password,user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Invalid credentials",
        )

    access_token = oath2.create_access_token(data={"user_id":user.id})

    return {"access_token": access_token, "token_type": "bearer"}

# Create a token
