from typing import Annotated
from fastapi import Depends, Form, HTTPException, status, APIRouter
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
from blogging_app import schemas, models
from instance.config import SECRET_KEY, ALGORITHM
from sqlalchemy.orm import Session
from blogging_app import dependencies

SECRET_KEY = SECRET_KEY
ALGORITHM = ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

auth_routes = APIRouter()

db_dependency = Annotated[Session, Depends(dependencies.get_db)]


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def authorize_url(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        return username
    except JWTError:
        raise credentials_exception


# - - - - - S I G N - U P - - - - -
@auth_routes.post("/sign-up")
async def sign_up(
  username: Annotated[str, Form(max_length=100)],
  first_name: Annotated[str, Form(max_length=100)],
  last_name: Annotated[str, Form(max_length=100)],
  email: Annotated[str, Form(max_length=100)],
  password: Annotated[str, Form(max_length=100)],
  confirm_password: Annotated[str, Form(max_length=100)],
  db: db_dependency
):
    """
    Handle the sign-up request.

    Parameters:
        - username (str): The username of the new user.
        - first_name (str): The first name of the new user.
        - last_name (str): The last name of the new user.
        - email (str): The email of the new user.
        - password (str): The password of the new user.
        - confirm_password (str): The confirmation password for the new user.
    
    Returns:
        dict: A dictionary containing the success message if the sign-up is successful.
    
    Raises:
        HTTPException: If the username already exists in the database.
    """
    username_in_DB_update = db.query(models.User).filter(models.User.username == username).first()
    email_in_DB_update = db.query(models.User).filter(models.User.email == email).first()
    if confirm_password != password:
        raise HTTPException(status_code=400, detail="Passwords do not match!")
    if username_in_DB_update:
        raise HTTPException(status_code=400, detail="Username already exists!")
    if email_in_DB_update:
        raise HTTPException(status_code=400, detail="Email already exists!")
    else:
        otp = dependencies.generate_otp()
        dependencies.send_mail(
            email,
            email_subject="BLOG APP OTP",
            email_body=f"Your OTP is: {otp}"
            )
        # user = models.User(
        #     username=username,
        #     first_name=first_name,
        #     last_name=last_name,
        #     email=email, 
        #     password=get_password_hash(password),
        #     last_updated_at=datetime.strptime(datetime.now().strftime("%d-%m-%Y %H:%M:%S"), "%d-%m-%Y %H:%M:%S").strftime("%d-%B-%Y %H:%M:%S")
        # )
        # try:
        #     db.add(user)
        #     db.commit()
        #     # db.refresh(user)
        # except Exception as e:
        #     db.rollback()
        #     raise HTTPException(status_code=500, detail="Internal server error")
    return {"message": "Sign-up successful!."}


# - - - - - L O G I N / S I G N - I N- - - - - -
@auth_routes.post("/token", response_model=schemas.Token)
async def sign_in(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency):
    """
    Signs in a user with their provided username and password.

    Parameters:
    - username (str): The username of the user.
    - password (str): The password of the user.

    Returns:
    - dict: A dictionary with a message if the sign-in was successful, otherwise raise an HTTPException.

    Raises:
    - HTTPException: If the provided username and/or password is incorrect.
    """
    credential_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect username or password",
        headers={"WWW-Authenticate": "Bearer"}
        )

    user = db.query(models.User).filter(models.User.username == form_data.username).first()
    if user.password and verify_password(form_data.password, user.password):
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)
    else:
        raise credential_exception
    return {
        "access_token": access_token,
        "token_type": "bearer"
        }