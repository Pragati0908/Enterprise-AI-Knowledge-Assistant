from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(
    prefix="/login",
    tags=["Authentication"]
)

class LoginRequest(BaseModel):
    username: str
    password: str


@router.post("/")
def login(user: LoginRequest):

    # Dummy authentication (Week 2 only)
    if user.username == "admin" and user.password == "admin123":

        return {
            "message": "Login Successful",
            "username": user.username,
            "access_token": "dummy_token_12345"
        }

    return {
        "message": "Invalid Username or Password"
    }