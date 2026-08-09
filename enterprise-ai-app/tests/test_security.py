from jose import jwt
from app.core.config import get_settings
from app.core.security import create_access_token

def test_token_contains_subject():
    token = create_access_token("demo", ["user"])
    config = get_settings()
    assert jwt.decode(token, config.jwt_secret, algorithms=[config.jwt_algorithm])["sub"] == "demo"
