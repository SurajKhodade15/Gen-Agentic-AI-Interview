from fastapi import APIRouter, HTTPException
from app.core.security import create_access_token
from app.schemas.chat import LoginRequest, TokenResponse

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/token", response_model=TokenResponse)
def login(request: LoginRequest):
    # Demo only: production validates Cognito/OIDC identity tokens.
    if request.username != "demo" or request.password != "demo-password":
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return TokenResponse(access_token=create_access_token(request.username, ["user"]))
