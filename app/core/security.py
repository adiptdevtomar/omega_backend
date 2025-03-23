from fastapi import Security, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext

# Security scheme for OAuth2
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Function to hash passwords
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

# Function to verify passwords
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# Function to get current user (placeholder for actual implementation)
def get_current_user(token: str = Security(oauth2_scheme)):
    # Here you would decode the token and retrieve the user
    raise HTTPException(status_code=401, detail="Invalid authentication credentials")

# Function to get current active user (placeholder for actual implementation)
def get_current_active_user(current_user: str = Security(get_current_user)):
    # Here you would check if the user is active
    return current_user